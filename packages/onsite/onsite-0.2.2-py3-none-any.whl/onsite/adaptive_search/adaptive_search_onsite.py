import numpy as np
import pandas as pd
from sklearn.metrics import classification_report
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from sklearn.model_selection import KFold
import datetime


class AdaptiveSearch:
    """根据测试矩阵，测试环境，代理模型，规控器四个信息初始化自适应搜索方法。

    :param scenario_space: np.array. 测试矩阵(test_matrix)
    :param env: 测试环境，包含env.test(scenario, sut) 方法
    :param sur_model: 用在自适应搜索中的代理模型
    :param sut: 用于测试环境的规控器，默认为 None，即环境不需要额外的规控器。
    """

    def __init__(self, scenario_space, sur_model):
        self.test_matrix = scenario_space
        self.sur_model = sur_model
        self.n_test_matrix = self.test_matrix.shape[0]
        self.n_scenario_shape = self.test_matrix.shape[1]
        self.sample = np.zeros((0, self.n_scenario_shape))
        self.result = np.zeros(0)
        # 超参数调整模块，记录器
        self.hyper_adjust_count = 0
        # 交叉验证终止条件，记录器
        self.stopping_criteria_count = 0

    def initialize(self, sample_num, sample_method='random', criteria='danger', hyper_adjust_iter=100, stopping_criteria_iter=100, stopping_criteria_limit=0.01):
        """产生一定的初始样本以初始化代理模型

        """
        # 清空之前记录的信息
        # 超参数调整模块，记录器归0
        self.hyper_adjust_count = 0 # 记录超参数调整上一次运行的轮次数
        self.hyper_adjust_iter = hyper_adjust_iter # 多少轮运行一次
        # 交叉验证终止条件，记录器归0 
        self.stopping_criteria_count = 0 # 记录交叉验证终止条件计算模块上一次运行的轮次数
        self.stopping_criteria_iter = stopping_criteria_iter # 多少轮运行一次
        self.stopping_criteria_limit = stopping_criteria_limit # 阈值
        # 场景库与测试结果归0
        self.sample = np.zeros((0, self.n_scenario_shape))
        self.result = np.zeros(0)
        # 选取场景的标准
        self.criteria = criteria
        # 初始化
        # 按照不同的初始化方式，进行初始化。
        if sample_method == 'linspace':
            sample = self.test_matrix[np.linspace(
                0, self.n_test_matrix - 1, sample_num).astype(int)]
        else:
            random_list = np.random.choice(
                self.test_matrix.shape[0], size=sample_num, replace=False)
            sample = self.test_matrix[random_list, :]
        print("Method:%s, InitRateCases:%d" %
              (sample_method, np.array(sample).shape[0]))
        return sample

    def generate_sample(self, sample_num, search_num=1e10, mini_dis=20):
        """根据代理模型提供的信息，从一定量的候选场景中选取新的待测场景。新的场景不会被测试，也不会被加入AdaptiveSearch对象的已测场景库中

        :param sample_num: 生成的新待测场景的数量
        :param criteria: 输入代理模型的参数，判定依据, string类型。如："danger"代表场景越危险约有价值，"boundary"代表边界场景更有价值。可取值根据代理模型支持的判定依据决定。
        :param search_num: 从几倍于新场景的候选场景中选取新场景。例如：本次想要选取5个新场景，search_num=10，则方法会从5×10=50个候选场景中选取5个新场景。
        :return:
            选出的新场景，np.array.
        """
        num_candidate_scenario = sample_num*search_num  # 候选场景的数量（从多少场景中挑选下一个待测场景）
        # 如果所用的候选场景数量多于场景库全体，则使用完整场景库作为候选场景库。
        num_candidate_scenario = min(
            num_candidate_scenario, self.n_test_matrix)
        # 生成符合候选场景数量的随机数
        sample_index = np.random.choice(self.n_test_matrix, num_candidate_scenario,
                                        replace=False)
        # 从场景库全集中将候选场景库取出
        sample_sub = self.test_matrix[sample_index, :]
        # 计算采集函数值
        criteria_value, dis = self.sur_model.get_criteria_value(
            sample_sub, self.criteria, mini_dis=mini_dis)
        # 以下费劲操作，只是为了取出采集函数值最大的n个。
        sample_frame = np.concatenate((sample_sub, criteria_value), axis=1)
        sample_frame = pd.DataFrame(sample_frame)
        sample_frame = sample_frame.sort_values(sample_frame.columns[-1],
                                                ascending=False)
        sample = np.array(sample_frame.iloc[:sample_num, :-1]).copy()
        return sample

    def _cal_cv_stopping(self, num=50000, obj_value=0, n_splits=10):

        kf = KFold(n_splits=n_splits)
        if self.test_matrix.shape[0] <= num:
            x_trans_sub = self.test_matrix.copy()
        else:
            x_trans_sub = self.test_matrix[np.random.choice(
                self.n_test_matrix, size=num, replace=False), :]

        x_trans_sub = self.sur_model.scaler.transform(x_trans_sub)
        y_pred_true = self.sur_model.sm.predict(x_trans_sub)
        danger_rate_true = (y_pred_true > obj_value).sum()/x_trans_sub.shape[0]
        error_max = 0
        for train, test in kf.split(self.sample):
            self.sur_model.train(self.sample[train], self.result[train])
            y_pred = self.sur_model.sm.predict(x_trans_sub)
            danger_rate = (y_pred > obj_value).sum()/x_trans_sub.shape[0]
            error = np.abs(danger_rate - danger_rate_true)/danger_rate_true
            if error_max < error:
                error_max = error

        self.sur_model.train(self.sample, self.result)
        return error_max

    def _add_sample_without_other_module(self, sample, result, train=False):
        """将场景以及对应的测试结果加入AdaptiveSearch对象的已测场景库中，并训练代理模型。
        不进行其他环节，如超参数调整，终止条件等等。

        :param sample: 场景样本
        :param result: 测试结果
        :param train: 在样本添加完毕后，是否训练代理模型，默认为False
        """
        sample = sample.reshape(-1, self.sample.shape[1])
        self.sample = np.concatenate((self.sample, sample), axis=0)
        self.result = np.append(self.result, result)
        if train:
            self.sur_model.train(self.sample, self.result)

    def add_sample(self, sample, result):
        """将场景以及对应的测试结果加入AdaptiveSearch对象的已测场景库中
        过程中也运行其他环节，如超参数调整模块等等。

        """
        # 超参数调整模块，如果已测样本数量达到超参数调整的要求，则进行超参数调整；否则只进行模型训练
        if (self.sample.shape[0] - self.hyper_adjust_count) >= self.hyper_adjust_iter:
            print('HyperParameters Adjust!')
            # 将新场景与测试结果加入场景库中，不训练代理模型（超参数调整后，会以最优参数进行拟合）
            self._add_sample_without_other_module(sample,result,train=False)
            # 运行超参数调整模块
            self.sur_model.change_model_new(
                    sample_change=self.sample, result_change=self.result)
            # 记录超参数调整模块运行时，目前已测的样本量。这个值将用来判断下一次超参数调整何时运行。
            self.hyper_adjust_count = self.sample.shape[0]
        else:
            # 将新场景与测试结果加入场景库中，并训练代理模型
            self._add_sample_without_other_module(sample, result, train=True)

        # 计算交叉验证终止条件
        # 该模块仅当搜索目标为建立精确代理模型时运行
        if self.criteria == 'sm':
            # 计算交叉验证终止条件的值
            sm_st = self.cal_cv_stopping()                
            print("Sample sum: %d" %
                    self.sample.shape[0], "Error : %.4f" % sm_st)
            # 记录交叉验证终止条件模块运行时，目前已测的样本量。这个值将用来判断下一次该模块何时运行。
            self.stopping_criteria_count = self.sample.shape[0]
            if sm_st <= self.stopping_criteria_count:
                return 1
        else:
            return 0
