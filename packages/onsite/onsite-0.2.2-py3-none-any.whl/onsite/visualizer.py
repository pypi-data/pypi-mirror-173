from onsite.observation import Observation
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import numpy as np


class Visualizer():
    def __init__(self):
        self.visilize = False
        self.road_exist = False

    def init(self, observation: Observation, visilize: bool = False):
        self.visilize = visilize
        if visilize:
            plt.ion()
            self.fig, self.axbg = plt.subplots()
            self.axveh = self.axbg.twiny()
            self.road_exist = False
        else:
            plt.ioff()
        self.update(observation)


    def update(self, observation: Observation) -> None:
        # 如果不画图，直接退出
        if not self.visilize:
            return
        # 如果测试结束，则结束绘图，关闭绘图模块
        if observation.test_setting['end'] != -1:
            plt.ioff()
            plt.close()
            return
        self.axveh.cla()
        # plt.cla()
        self._plot_vehicles(observation)  # 绘制车辆
        if not self.road_exist:
            self._plot_roads(observation)  # 绘制道路
            self.road_exist = True
        # 其他画图设置
        # 设置x,y坐标的比例为相同
        plt.gca().set_aspect('equal')
        # 指定y坐标的显示范围
        plt.ylim(-40, 40)
        # 指定x坐标显示范围
        x_center = observation.vehicle_info['ego']['x']
        plt.xlim(x_center - 70, x_center + 70)
        # 让图片显示出来
        plt.pause(1e-7)
        # plt.show()

    def _plot_vehicles(self, observation: Observation) -> None:
        for key, values in observation.vehicle_info.items():
            if key == 'ego':
                self._plot_single_vehicle(key, values, c='red')
            else:
                self._plot_single_vehicle(key, values, c='blue')

    def _plot_single_vehicle(self, key: str, vehi: dict, c='blue'):
        """利用 matplotlib 和 patches 绘制小汽车，以 x 轴为行驶方向

        """
        x, y, yaw, width, length = [float(vehi[i])
                                    for i in ['x', 'y', 'yaw', 'width', 'length']]

        angle = np.arctan(width / length) + yaw
        diagonal = np.sqrt(length ** 2 + width ** 2)
        self.axveh.add_patch(
            patches.Rectangle(
                xy=(x - diagonal / 2 * np.cos(angle),
                    y - diagonal / 2 * np.sin(angle)),
                width=length,
                height=width,
                angle=yaw / np.pi * 180,
                color=c,
                fill=False
            ))
        self.axveh.annotate(key, (x, y))

    def _plot_roads(self, observation: Observation) -> None:
        '''根据observation绘制道路，只要完成绘制工作即可。plt.plot()。其他plt.show()之类的不需要添加

        Parameters
        ----------
        observation:当前时刻的观察值
        '''
        road_data_for_plot = observation.road_info
        # plotting roads
        if not road_data_for_plot:
            return

        xlim1 = float("Inf")
        xlim2 = -float("Inf")
        ylim1 = float("Inf")
        ylim2 = -float("Inf")
        color = "gray"
        alpha = 0.3
        zorder = 0
        label = None
        draw_arrow = False

        for discrete_lane in road_data_for_plot.discretelanes:
            verts = []
            codes = [Path.MOVETO]

            for x, y in np.vstack(
                [discrete_lane.left_vertices, discrete_lane.right_vertices[::-1]]
            ):
                verts.append([x, y])
                codes.append(Path.LINETO)

                # if color != 'gray':
                xlim1 = min(xlim1, x)
                xlim2 = max(xlim2, x)

                ylim1 = min(ylim1, y)
                ylim2 = max(ylim2, y)

            verts.append(verts[0])
            codes[-1] = Path.CLOSEPOLY

            path = Path(verts, codes)

            self.axbg.add_patch(
                patches.PathPatch(
                    path,
                    facecolor=color,
                    edgecolor="black",
                    lw=0.0,
                    alpha=alpha,
                    zorder=zorder,
                    label=label,
                )
            )

            self.axbg.plot(
                [x for x, y in discrete_lane.left_vertices],
                [y for x, y in discrete_lane.left_vertices],
                color="black",
                lw=0.1,
            )
            self.axbg.plot(
                [x for x, y in discrete_lane.right_vertices],
                [y for x, y in discrete_lane.right_vertices],
                color="black",
                lw=0.1,
            )

            if draw_arrow:
                idx = 0

                ml = discrete_lane.left_vertices[idx]
                mr = discrete_lane.right_vertices[idx]
                mc = discrete_lane.center_vertices[
                    min(len(discrete_lane.center_vertices) - 1, idx + 10)
                ]

                self.axbg.plot(
                    [ml[0], mr[0], mc[0], ml[0]],
                    [ml[1], mr[1], mc[1], ml[1]],
                    color="black",
                    lw=0.3,
                    zorder=15,
                )
        return
