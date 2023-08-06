from sklearn.model_selection import GridSearchCV
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor
from sklearn.metrics import make_scorer,f1_score

class XGBSurModel():
    def __init__(self, scaler, kernel='rbf', obj_value=0):
        self.scaler = scaler
        self.knn = KNeighborsRegressor(n_neighbors=1)
        self.sm = SM()  # n_estimators=100,
        self.sm_base = XGBRegressor
        self.obj_value = obj_value
        self.alpha = 3

    def train(self, sample, result):
        result = result.reshape(-1, 1)
        sample_trans = self.scaler.transform(sample)
        self.sm.fit(sample_trans, result.reshape(-1))
        self.knn.fit(sample_trans, result)

    def predict(self,sample):
        sample_trans = self.scaler.transform(sample)
        grad = self.sm.predict(sample_trans).reshape(-1)
        return grad
        
    def change_model_new(self, sample_change, result_change,sample_num=50000, obj_value=0):
        # 定义参数组合
        param_grid = {
            # 'n_estimators':[100,200,300],
            'min_child_weight':[1,3,5,7],
            'max_depth': [3, 5, 9, 12, 15, 17, 25],
            'learning_rate':[0.01, 0.015, 0.025, 0.05, 0.1]
            }
        
        sample = sample_change.copy()
        result = result_change.copy()

        if sample.shape[0] > sample_num:
            rd = np.random.choice(sample.shape[0], sample_num, replace=False)
            sample = sample[rd, :]
            result = result[rd, :]

        sample_trans = self.scaler.transform(sample)

        svc_model = self.sm_base()

        grid_search = GridSearchCV(svc_model, param_grid,scoring=self.f1_scorer(),n_jobs=8, verbose=0)  # n_jobs:并行数，int类型。(-1：跟CPU核数一致；1:默认值)；verbose:日志冗长度。默认为0：不输出训练过程；1：偶尔输出；>1：对每个子模型都输出。
        grid_search.fit(sample_trans, result)  # 训练，使用f1score作为评价，因此选择result>0
        best_parameters = grid_search.best_estimator_.get_params()  # 获取最佳模型中的最佳参数
        #print("cv results are" % grid_search.best_params_, grid_search.cv_results_)  # grid_search.cv_results_:给出不同参数情况下的评价结果。
        print("best parameters are" % grid_search.best_params_, grid_search.best_params_)  # grid_search.best_params_:已取得最佳结果的参数的组合；
        print("best score are" % grid_search.best_params_, grid_search.best_score_)  # grid_search.best_score_:优化过程期间观察到的最好的评分。
        self.sm = self.sm_base(
            # n_estimators=best_parameters['n_estimators'],
            min_child_weight=best_parameters['min_child_weight'], 
            max_depth=best_parameters['max_depth'], 
            learning_rate=best_parameters['learning_rate'])  # 最佳模型
        self.train(sample, result)  # train的时候自动做归一化

    def get_criteria_value(self, sample, criteria='danger',mini_dis = 20):
#         assert (criteria in self.criteria_list)
        sample_trans = self.scaler.transform(sample)
        
        dis, _ = self.knn.kneighbors(sample_trans,n_neighbors=1) # 
#         dis, _ = self.knn.kneighbors(sample,n_neighbors=1) # 
        exist_trigger = (dis[:, 0] == 0)
        dis = dis.mean(axis=1)
        dis = (dis-dis.min())/(dis.max()-dis.min()) # 归一化处理
        dis = dis.reshape(-1)
    
#         dis[exist_trigger] = 0
        grad = self.sm.predict(sample_trans).reshape(-1)
        if (grad>0).sum() > 0:
            grad_max_po = grad[grad>0].max()
            grad_min_po = grad[grad>0].min()
            grad[grad>0] = (grad[grad>0]-grad_min_po)/(grad_max_po-grad_min_po)
        if (grad<0).sum() > 0:
            grad_max_ne = grad[grad<=0].max()
            grad_min_ne = grad[grad<=0].min()
            grad[grad<0] = (grad[grad<0]-grad_min_ne)/(grad_max_ne-grad_min_ne) - 1
        
        if criteria == 'danger':
            grad -= grad.min()
            criteria_value = grad**self.alpha * dis
            criteria_value[exist_trigger] = -100
            
        elif criteria == 'sm':
            # grad 越小， 代表预测值越接近 obj_value
            grad = np.abs(grad-self.obj_value)
            grad = (grad-grad.min())/(grad.max()-grad.min()) # 归一化处理
            criteria_value = -(grad+1e-4) / (dis+1e-4)
    #         dis_mini = 0.5*np.max(dis)
            dis_mini = np.percentile(dis, mini_dis)
            criteria_value[dis < dis_mini] = -100
            criteria_value[exist_trigger] = -100

        elif criteria == 'sm_no_spacefilling':
            # grad 越小， 代表预测值越接近 obj_value
            grad = np.abs(grad-self.obj_value)
            grad = (grad-grad.min())/(grad.max()-grad.min()) # 归一化处理
            criteria_value = -(grad+1e-4) / (dis+1e-4)
    #         dis_mini = 0.5*np.max(dis)
            # dis_mini = np.percentile(dis, mini_dis)
            # criteria_value[dis < dis_mini] = -100
            criteria_value[exist_trigger] = -100

        elif criteria == 'add':
            grad -= grad.min()
            criteria_value = grad + dis
            criteria_value[exist_trigger] = -100      

        return criteria_value.reshape(-1,1),dis

    def logloss(self,true_value, predict):
        f1 = f1_score(true_value>0,predict>0)
        return f1
    
    def f1_scorer(self):
        return make_scorer(self.logloss)    

class SM(XGBRegressor):
    pass