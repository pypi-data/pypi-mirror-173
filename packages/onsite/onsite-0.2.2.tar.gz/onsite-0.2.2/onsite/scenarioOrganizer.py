import os
import shutil
import sys
from unicodedata import category
import numpy as np
from sklearn.preprocessing import StandardScaler
from onsite.adaptive_search.adaptive_search_onsite import AdaptiveSearch
from onsite.adaptive_search.xgb_sur_model import XGBSurModel


class ScenarioOrganizer():
    def __init__(self):
        self.test_mode = ""
        self.scenario_list = []
        self.test_matrix = np.array([])
        self.test_num = 0
        self.scaler = None
        self.adaptive_method = None

    def load(self, input_dir: str, output_dir:str) -> None:
        """读取配置文件，按照配置文件（py格式）准备场景内容

        """
        # 清空场景列表
        self.scenario_list = []
        # 将目标目录加入检索目录
        sys.path.append(input_dir)
        # 清空或创建输出文件夹
        self._set_dir(output_dir)
        # 读取配置文件
        from conf import config
        self.config = config
        self.test_mode = config['test_settings']['mode']

        # 如果测试模式 == 'replay'，读取文件夹下所有待测场景，存在列表中
        if self.test_mode == 'replay':  # 判断测试模式是否为replay
            for item in os.listdir(input_dir):  # 遍历input文件夹
                if item.split(".")[-1] != 'py':  # 如果后缀名不是py
                    if item != "__pycache__":  # 也不是pycache文件
                        sce_path = input_dir + "/" + item
                        sce = self.config.copy()
                        sce['data'] = {
                            'params': sce_path
                        }
                        # 将场景加入列表中
                        self.scenario_list += [sce]

        # 如果测试模式 == 'adaptive'，
        elif self.test_mode == 'adaptive':
            # 第一步：读取配置文件中的信息
            # 取出测试次数上限
            self.test_num = config['test_settings']['test_num']
            # 取出上下界，以及取值间隔信息
            upper_bound = np.array(
                config['scenario_settings']['upper_bound'])  # 上界
            lower_bound = np.array(
                config['scenario_settings']['lower_bound'])  # 下界
            interval = np.array(config['scenario_settings']['interval'])  # 间隔

            # 第二步：交叉组合，构建测试矩阵。写法有点难懂
            grad = []
            for i in range(upper_bound.shape[0]):
                grad += [np.arange(lower_bound[i],
                                   upper_bound[i], interval[i])]
            a = np.meshgrid(*grad)
            self.test_matrix = np.vstack([x.ravel() for x in a]).T
            print("测试矩阵构建完毕：", self.test_matrix.shape)
            # 第三步：训练数据标准化模块
            self.scaler = StandardScaler()
            self.scaler.fit(self.test_matrix)
            # 第四步：初始化自适应搜索算法
            surrogate_model = XGBSurModel(self.scaler)  # 初始化代理模型
            self.adaptive_method = AdaptiveSearch(
                self.test_matrix, surrogate_model)
            # 第五步：采集初始样本
            sample = self.adaptive_method.initialize(
                sample_num=10,
                criteria=config['test_settings']['criteria'],
                hyper_adjust_iter=config['test_settings']['hyper_adjust_iter']
            )
            for i in sample:
                sce = self.config.copy()
                sce['data'] = {
                    'params': i
                }
                self.scenario_list += [sce]

    def next(self):
        """给出下一个待测场景与测试模式，如果没有场景了，则待测场景名称为None

        """
        # 首先判断测试的模式，replay模式和adaptive模式不一样
        if self.test_mode == 'replay':  # 如果是回放测试
            if self.scenario_list:  # 首先判断列表是否为空，如果列表不为空，则取场景；否则，输出None
                # 列表不为空，输出0号场景，且将其从列表中删除（通过pop函数实现）
                scenario_to_test = self.scenario_list.pop(0)
            else:
                # 列表为空，输出None
                scenario_to_test = None
        # 如果是adaptive，自适应搜索模式
        elif self.test_mode == 'adaptive':
            if self.test_num == 0:  # 如果测试资源用完，则测试结束
                scenario_to_test = None
            else:
                # 如果场景列表为空，则用自适应搜索方法采集新的场景
                if not self.scenario_list:
                    sample = self.adaptive_method.generate_sample(1)
                    for i in sample:
                        sce = self.config.copy()
                        sce['data'] = {
                            'params': i
                        }
                        self.scenario_list += [sce]
                # 输出0号场景，且将其从列表中删除（通过pop函数实现）
                scenario_to_test = self.scenario_list.pop(0)
                self.test_num -= 1

        return scenario_to_test

    def add_result(self, concrete_scenario: dict, res: float) -> None:
        # 判断测试模式，如果是replay，则忽略测试结果
        if self.test_mode == 'replay':
            return
        elif self.test_mode == 'adaptive':
            sample_to_add = concrete_scenario['data']['params']
            stopping_res = self.adaptive_method.add_sample(sample_to_add, res)
            # 如果满足终止条件，则清空测试次数，测试终止。
            if stopping_res == 1:
                self.test_num = 0
    def _set_dir(self,filepath):
        '''清空或创建目标文件夹
        
        '''
        if not os.path.exists(filepath):
            os.mkdir(filepath)
        else:
            os.removedirs(filepath)
            # shutil.rmtree(filepath)
            os.mkdir(filepath)

if __name__ == "__main__":
    demo_replay = r"demo/demo_inputs_adaptive"
    demo_ouput_dir = r"demo/demo_outputs"
    so = ScenarioOrganizer()
    so.load(demo_replay, demo_ouput_dir)
    while True:
        scenario_to_test = so.next()
        if scenario_to_test is None:
            break  # 如果场景管理模块给出None，意味着所有场景已测试完毕。
        if scenario_to_test['test_settings']['mode'] == 'adaptive':
            res = scenario_to_test['data']['params'][0]**2 - \
                scenario_to_test['data']['params'][1]**2
        else:
            res = 1
        print(scenario_to_test, res)
        so.add_result(scenario_to_test, res)
