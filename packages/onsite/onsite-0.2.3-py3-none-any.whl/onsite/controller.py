from unicodedata import category

from tables import ObjectAtom
from onsite.observation import Observation
from onsite.opendrive2discretenet.opendriveparser.parser import parse_opendrive
from onsite.opendrive2discretenet.network import Network
import importlib

import os
import xml.dom.minidom
from lxml import etree
import re
import numpy as np
import pandas as pd
import copy
from shapely.ops import unary_union
from shapely.geometry import Polygon
from itertools import combinations


class ReplayInfo():
    """用于存储回放测试中用以控制背景车辆的所有数据
        背景车轨迹信息 vehicle_traj
        vehicle_traj = {
            "vehicle_id_0":{
                "shape":{
                    "wid":4,
                    "len":5
                },
                "t_0":{
                    "x":10,
                    "y":10,
                    "v":10,
                    "yaw":0
                },
                "t_1":{...},
                ...
            },
            "vehicle_id_1":{...},
            ...
        }

        ego_info = {
            "shape":{
                "wid":
                "len":
            },
            "state":{
                "x":10,
                "y":10,
                "v":10,
                "yaw":0
            }
        }

        测试环境相关信息 test_setting
        test_setting = {
            "dt":,
            "max_t",
            "goal":
        }

    """

    def __init__(self):
        self.vehicle_traj = {}
        self.ego_info = {
            "length": 4.924,
            "width": 1.872,
            "x": 0,
            "y": 0,
            "v": 0,
            "yaw": 0
        }
        self.road_info = {}
        self.test_setting = {
            "t": 0,
            "dt": 0.01,
            "max_t": 10,
            "goal": {
                "x": [-10, 10],
                "y": [-10, 10]
            },
            "end": -1
        }

    def add_vehicle(self, id, t, x=None, y=None, v=None, yaw=None, length=None, width=None):
        if id == "ego":
            self._add_vehicle_ego(x, y, v, yaw, length, width)
        else:
            if id not in self.vehicle_traj.keys():
                self.vehicle_traj[id] = {}
                self.vehicle_traj[id]['shape'] = {}
            if t not in self.vehicle_traj[id].keys():
                self.vehicle_traj[id][t] = {}
            for key, value in zip(['x', 'y', 'v', 'yaw'], [x, y, v, yaw]):
                if value is not None:
                    self.vehicle_traj[id][t][key] = value
            for key, value in zip(['length', 'width'], [length, width]):
                if value is not None:
                    self.vehicle_traj[id]['shape'][key] = value

    def add_settings(self, scenario_name=None, scenario_type=None, dt=None, max_t=None, goal_x=None, goal_y=None):
        for key, value in zip(['scenario_name', 'scenario_type', 'dt', 'max_t'], [scenario_name, scenario_type, dt, max_t]):
            if value is not None:
                self.test_setting[key] = value
        for key, value in zip(['x', 'y'], [goal_x, goal_y]):
            if value is not None:
                self.test_setting['goal'][key] = value

    def _add_vehicle_ego(self, x=None, y=None, v=None, yaw=None, length=None, width=None):
        for key, value in zip(['x', 'y', 'v', 'yaw', 'length', 'width'], [x, y, v, yaw, length, width]):
            if value is not None:
                self.ego_info[key] = value

    def _get_dt_maxt(self):
        max_t = 0
        for i in self.vehicle_traj.keys():
            t_i = list(self.vehicle_traj[i].keys())
            max_t_i = float(t_i[-1])
            if max_t_i > max_t:
                max_t = max_t_i
        dt = np.around(float(t_i[-1]) - float(t_i[-2]), 3)
        self.add_settings(dt=dt, max_t=max_t)


class ReplayParser():
    """解析场景文件

    """

    def __init__(self):
        self.replay_info = ReplayInfo()

    def parse(self, input_dir: str) -> ReplayInfo:
        # 在目录中寻找.xosc文件和.xodr文件
        for item in os.listdir(input_dir):
            if item.split(".")[-1] == 'xosc':
                path_openscenario = input_dir + "/" + item
            if item.split(".")[-1] == 'xodr':
                path_opendrive = input_dir + "/" + item
        self._parse_openscenario(path_openscenario)
        self._parse_opendrive(path_opendrive)
        return self.replay_info

    def _parse_openscenario(self, file_dir: str):
        # 读取OpenScenario文件
        opens = xml.dom.minidom.parse(file_dir).documentElement

        # 读取车辆长度与宽度信息，录入replay_info。背景车id从1号开始
        wl_node = opens.getElementsByTagName('Dimensions')
        for num, wl in zip(range(len(wl_node)), wl_node):
            if num == 0:
                self.replay_info.add_vehicle(
                    id="ego",
                    t=-1,
                    width=float(wl.getAttribute('width')),
                    length=float(wl.getAttribute('length'))
                )
            else:
                self.replay_info.add_vehicle(
                    id=num,
                    t=-1,
                    width=float(wl.getAttribute('width')),
                    length=float(wl.getAttribute('length'))
                )

        # 读取本车信息, 记录为ego_v,ego_x,ego_y,ego_head
        ego_node = opens.getElementsByTagName('Private')[0]
        ego_init = ego_node.childNodes[3].data
        ego_v, ego_x, ego_y, ego_head = [
            float(i.split('=')[1]) for i in ego_init.split(',')]
        self.replay_info.add_vehicle(
            id="ego",
            t=-1,
            x=ego_x,
            y=ego_y,
            v=ego_v,
            yaw=ego_head
        )

        # 读取其他车辆信息，编号从1号开始
        # 记录每辆车的轨迹，存在dic里面。
        # 注：本车不存在Act项。
        # 注：场景文件中没有速度信息。
        actor_list = opens.getElementsByTagName('Act')
        for id, act in zip(np.arange(1, len(actor_list) + 1), actor_list):
            for point in act.getElementsByTagName('Vertex'):
                t = point.getAttribute('time')
                t = str(round(float(t), 3))  # t保留三位小数，以字符串的形式作为字典的key
                loc = point.getElementsByTagName('WorldPosition')[0]
                self.replay_info.add_vehicle(
                    id=id,
                    t=t,
                    x=float(loc.getAttribute('x')),
                    y=float(loc.getAttribute('y')),
                    yaw=float(loc.getAttribute('h')),
                    v=-1
                )

        # 获取其他信息
        # 场景名称与测试类型
        name = file_dir.split('/')[-1]  # 取得xxx.xosc
        name = name.split('.')[0]  # 取得场景名
        self.replay_info.add_settings(
            scenario_name=name, scenario_type='replay')
        # 获取行驶目标, goal
        goal_init = ego_node.childNodes[5].data
        goal = [float(i) for i in re.findall('-*\d+\.\d+', goal_init)]
        self.replay_info.add_settings(
            goal_x=goal[:2],
            goal_y=goal[2:]
        )
        # 步长与最大时间
        self.replay_info._get_dt_maxt()

        return self.replay_info

    def _parse_opendrive(self, path_opendrive: str) -> None:
        """
        解析opendrive路网的信息，存储到self.replay_info.road_info。

        Parameters
        ----------
        path_opendrive: opendrive的.xodr格式的文件的位置
        """
        fh = open(path_opendrive, "r")
        # 返回OpenDrive类的实例对象（经过parser.py解析）
        openDriveXml = parse_opendrive(etree.parse(fh).getroot())
        fh.close()

        # 将OpenDrive类对象进一步解析为参数化的Network类对象，以备后续转化为DiscreteNetwork路网并可视化
        self.loadedRoadNetwork = Network()
        self.loadedRoadNetwork.load_opendrive(openDriveXml)

        '''将解析完成的Network类对象转换为DiscreteNetwork路网，其中使用的只有路网中各车道两侧边界的散点坐标
        车道边界点通过线性插值的方式得到，坐标点储存在<DiscreteNetwork.discretelanes.left_vertices/right_vertices> -> List
        '''
        open_drive_info = self.loadedRoadNetwork.export_discrete_network(filter_types=["driving", "onRamp", "offRamp", "exit", "entry"])  # -> <class> DiscreteNetwork
        self.replay_info.road_info = open_drive_info


class ReplayController():
    def __init__(self):
        self.control_info = ReplayInfo()

    def init(self, control_info: ReplayInfo) -> Observation:
        self.control_info = control_info
        return self._get_initial_observation()

    def step(self, action, old_observation: Observation) -> Observation:
        new_observation = self._update_ego_and_t(action, old_observation)
        new_observation = self._update_other_vehicles_to_t(new_observation)
        new_observation = self._update_end_status(new_observation)
        return new_observation

    def _get_initial_observation(self) -> Observation:
        observation = Observation()
        # vehicle_info
        observation.vehicle_info["ego"] = self.control_info.ego_info
        observation = self._update_other_vehicles_to_t(observation)
        # road_info
        observation.road_info = self.control_info.road_info
        # test_setting
        observation.test_setting = self.control_info.test_setting
        observation = self._update_end_status(observation)
        return observation

    def _update_ego_and_t(self, action: tuple, old_observation: Observation) -> Observation:
        # 拷贝一份旧观察值
        new_observation = copy.copy(old_observation)
        # 首先修改时间，新时间=t+dt
        new_observation.test_setting['t'] = float(
            old_observation.test_setting['t'] +
            old_observation.test_setting['dt']
        )
        # 修改本车的位置，方式是前向欧拉更新，1.根据旧速度更新位置；2.然后更新速度。
        # 速度和位置的更新基于自行车模型。
        # 首先分别取出加速度和方向盘转角
        a, rot = action
        # 取出步长
        dt = old_observation.test_setting['dt']
        # 取出本车的各类信息
        x, y, v, yaw, width, length = [float(old_observation.vehicle_info['ego'][key]) for key in [
            'x', 'y', 'v', 'yaw', 'width', 'length']]

        # 首先根据旧速度更新本车位置
        new_observation.vehicle_info['ego']['x'] = x + \
            v * np.cos(yaw) * dt  # 更新X坐标

        new_observation.vehicle_info['ego']['y'] = y + \
            v * np.sin(yaw) * dt  # 更新y坐标

        new_observation.vehicle_info['ego']['yaw'] = yaw + \
            v / length * 1.7 * np.tan(rot) * dt  # 更新偏航角

        new_observation.vehicle_info['ego']['v'] = v + a * dt  # 更新速度
        return new_observation

    def _update_other_vehicles_to_t(self, old_observation: Observation) -> Observation:
        # 删除除了ego之外的车辆观察值
        new_observation = copy.copy(old_observation)  # 复制一份旧观察值
        new_observation.vehicle_info = {}
        # 将本车信息添加回来
        new_observation.vehicle_info['ego'] = old_observation.vehicle_info['ego']
        # 根据时间t，查询control_info,赋予新值
        t = old_observation.test_setting['t']
        t = str(np.around(t, 3))  # t保留3位小数，与生成control_info时相吻合
        for vehi in self.control_info.vehicle_traj.items():
            id = vehi[0]  # 车辆id
            info = vehi[1]  # 车辆的轨迹信息
            if t in info.keys():
                new_observation.vehicle_info[id] = {}
                for key in ['x', 'y', 'v', 'yaw']:
                    new_observation.vehicle_info[id][key] = info[t][key]
                for key in ['width', 'length']:
                    new_observation.vehicle_info[id][key] = info['shape'][key]
        return new_observation

    def _update_end_status(self, observation: Observation) -> Observation:
        """计算T时刻, 测试是否终止, 更新observation.test_setting中的end值
            end=
                1:回放测试运行完毕；
                2:发生碰撞;
        """
        status_list = [-1]

        # 检查是否发生碰撞（目前会检测场景中所有车辆的碰撞情况，注：背景车与背景车相碰也会检测为碰撞）
        if self._collision_detect(observation):
            status_list += [2]

        # 检查是否已到达场景终止时间max_t
        if observation.test_setting['t'] >= self.control_info.test_setting['max_t']:
            status_list += [1]

        # 从所有status中取最大的那个作为end。
        observation.test_setting['end'] = max(status_list)
        return observation

    def _collision_detect(self, observation: Observation) -> bool:
        intersection = []
        poly_zip = []
        # 遍历所有位置>5的车辆，绘制对应的多边形。因为数据问题，有些车辆在初始位置有重叠。
        for vehi in observation.vehicle_info.values():
            if vehi['x'] > 5:
                poly_zip += [self._get_poly(vehi)]

        # 下面，通过判断多边形之间是否有交集来检测碰撞。
        # 方法为：
        # 1.unary_union括号内部的代码为，从所有车辆多边形中，排列组合取出两个，检测是否相交。
        # 2.通过unary_union方法，对这些两两排列组合得到的交集取并集，如果并集的面积>0，则有碰撞发生
        # 感觉这个方法可以优化
        intersection = unary_union(
            [a.intersection(b) for a, b in combinations(poly_zip, 2)]
        ).area

        # 如果并集面积>0，发生碰撞
        if intersection > 0:
            return True
        else:
            return False

    def _get_poly(self, vehicle: dict) -> Polygon:
        """根据车辆信息,通过shapely库绘制矩形。

        这是为了方便地使用shapely库判断场景中的车辆是否发生碰撞
        """
        # 从字典中取出数据，方便后续处理
        x, y, yaw, width, length = [float(vehicle[i])
                                    for i in ['x', 'y', 'yaw', 'width', 'length']]

        # 以下代码，是通过x，y，车辆转角，车长，车宽信息，计算出车辆矩形的4个顶点。
        alpha = np.arctan(width / length)
        diagonal = np.sqrt(width ** 2 + length ** 2)
        # poly_list = []
        x0 = x + diagonal / 2 * np.cos(yaw + alpha)
        y0 = y + diagonal / 2 * np.sin(yaw + alpha)
        x2 = x - diagonal / 2 * np.cos(yaw + alpha)
        y2 = y - diagonal / 2 * np.sin(yaw + alpha)
        x1 = x + diagonal / 2 * np.cos(yaw - alpha)
        y1 = y + diagonal / 2 * np.sin(yaw - alpha)
        x3 = x - diagonal / 2 * np.cos(yaw - alpha)
        y3 = y - diagonal / 2 * np.sin(yaw - alpha)

        # 通过车辆矩形的4个顶点，可以绘制出对应的长方形
        poly = Polygon(((x0, y0), (x1, y1),
                        (x2, y2), (x3, y3),
                        (x0, y0))).convex_hull
        return poly


class AdaptiveController():
    def __init__(self) -> None:
        self.env = None

    def init(self, scenario):
        category = scenario['scenario_settings']['category']
        params = scenario['data']['params']
        # 根据scenario的种类，导入对应的预先定义的场景运行文件
        cls = importlib.import_module('env_pre_defined.' + category)
        # 将测试场景类ENV取出
        ENV = getattr(cls, 'ENV')
        # 实例化测试场景类
        self.env = ENV()
        # 根据参数初始化场景
        self.env.init(params)
        # 建立观察值
        observation = Observation()
        # 首先将场景相关信息加入observation
        observation.test_setting['scenario_name'] = category+" "+str(params)
        observation.test_setting['scenario_type'] = 'adaptive'
        observation.test_setting['dt'] = scenario['scenario_settings']['dt']
        observation.test_setting['max_t'] = scenario['scenario_settings']['max_t']
        # !!!!!!!!!!!!!!! goal的定义，没有赋予行驶目标!!!!!!!!!!!!!!!!!!!!!
        observation.test_setting['goal']['x'] = [1e3, 1e4]
        observation.test_setting['goal']['y'] = [-5, 5]
        # 将车辆数据加入observation。
        observation = self._add_vehicle_to_observation(
            self.env, observation)
        # print(observation.test_setting)
        # print(observation.vehicle_info)
        # print(self.env.vehicle_list)
        return observation

    def step(self, action, old_observation: Observation) -> Observation:
        reward, done = self.env.update(action)
        new_observation = self._add_vehicle_to_observation(
            self.env, old_observation)
        # 终止条件的判断，目前只用了done的信息，只有0和1两个值。
        new_observation.test_setting['t'] = old_observation.test_setting['t'] + \
            old_observation.test_setting['dt']
        if done:  # 碰撞？
            new_observation.test_setting['end'] = 2
        # 回放测试运行完毕
        elif float(new_observation.test_setting['t']) >= float(new_observation.test_setting['max_t']):
            new_observation.test_setting['end'] = 1
        return new_observation

    def _add_vehicle_to_observation(self, env, old_observation: Observation) -> Observation:
        # print(env.vehicle_list,env.vehicle_array)
        new_observation = old_observation
        for i in range(len(env.vehicle_list)):
            name = env.vehicle_list[i]
            data = env.vehicle_array[0, i, :]
            for key, value in zip(
                ['x', 'y', 'v', 'yaw', 'length', 'width'],
                data
            ):
                if name not in new_observation.vehicle_info.keys():
                    new_observation.vehicle_info[name] = {}
                new_observation.vehicle_info[name][key] = value

        return new_observation


class Controller():
    """控制车辆运行

    """

    def __init__(self) -> None:
        self.observation = Observation()
        self.parser = None
        self.control_info = None
        self.controller = None
        self.mode = 'replay'

    def init(self, scenario: dict) -> Observation:
        """初始化运行场景，给定初始时刻的观察值

        Parameters
        ----------
        input_dir : str
            测试输入文件所在位置
                回放测试：包含.xodr、.xosc文件
                交互测试：
        mode : str
            指定测试模式
                回放测试：replay
                交互测试：interact
        Returns
        -------
        observation : Observation
            初始时刻的观察值信息，以Observation类的对象返回。
        """
        self.mode = scenario['test_settings']['mode']
        if self.mode == 'replay':
            self.parser = ReplayParser()
            self.controller = ReplayController()
            self.control_info = self.parser.parse(scenario['data']['params'])
            self.observation = self.controller.init(self.control_info)
        elif self.mode == 'adaptive':
            self.controller = AdaptiveController()
            self.observation = self.controller.init(scenario)
        return self.observation

    def step(self, action):
        self.observation = self.controller.step(action, self.observation)
        return self.observation


if __name__ == "__main__":
    # 指定输入输出文件夹位置
    demo_input_dir = r"demo/demo_inputs"
    demo_ouput_dir = r"demo/demo_outputs"
    from scenarioOrganizer import ScenarioOrganizer
    # 实例化场景管理模块（ScenairoOrganizer）和场景测试模块（Env）
    so = ScenarioOrganizer()
    # 根据配置文件config.py装载场景，指定输入文件夹即可，会自动检索配置文件
    so.load(demo_input_dir, demo_ouput_dir)
    scenario_to_test = so.next()
    print(scenario_to_test)
    controller = Controller()
    controller.init(scenario_to_test)

    # self.l = len_list[0]/self.l_l # 计算本车轴距
