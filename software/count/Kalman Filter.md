![image-20240519145438394](C:\Users\fan\AppData\Roaming\Typora\typora-user-images\image-20240519145438394.png)

<img src="C:\Users\fan\AppData\Roaming\Typora\typora-user-images\image-20240519155218873.png" alt="image-20240519155218873" style="zoom:50%;" />

~~~c
// 

typedef struct {
    float E_est_last; // 上次估计误差
    float E_est_now; // 当前估计误差
    float E_mea; // 测量误差
    float Data_last_Predict; // 上次估计值
    float Data_Current_Predict; // 当前估计值
    float Data_Curent_Measure; // 当前测量值
    float K; // Kalman增益系数
    
}KalmanFilter;

float Kalman_Init(KalmanFilter * kf,) {
    // 第一步：计算Kalman Gain
    kf->K = kf->E_est_last/(E_est_last +E_mea);
    // 第二步：计算当前估计值
    kf->Data_Current_Predict = kf->K+(kf->Data_Curent_Measure-Data_last_Predict);
    // 第三步：更新E_est
    kf->E_est_now = (1-kf->K)E_est_last
    return ;
}
~~~



~~~c
#include <stdio.h>

// 定义卡尔曼滤波器结构体
typedef struct {
    float Q; // 过程噪声协方差,Q越大滤波器更加依赖于新的测量数据而非模型预测
    float R; // 测量噪声协方差，实际测量值与真实值之间的误差，R越大滤波器会更倾向于信任模型预测而非测量数据
    float x; // 估计值
    float P; // 估计误差协方差，波器对当前状态估计的自信程度的度量，P越大意味着当前的估计值不太可靠
    float K; // 卡尔曼增益，如果K值较大，新的测量值对最终估计的影响更大
} KalmanFilter;

// 初始化卡尔曼滤波器
void KalmanFilter_Init(KalmanFilter *kf, float Q, float R, float initial_value) {
    kf->Q = Q;
    kf->R = R;
    kf->x = initial_value;
    kf->P = 1.0;
    kf->K = 0.0;
}

// 更新卡尔曼滤波器
float KalmanFilter_Update(KalmanFilter *kf, float measurement) {
    // 预测更新
    kf->P = kf->P + kf->Q;

    // 计算卡尔曼增益
    kf->K = kf->P / (kf->P + kf->R);

    // 更新估计值
    kf->x = kf->x + kf->K * (measurement - kf->x);

    // 更新估计误差协方差
    kf->P = (1 - kf->K) * kf->P;

    return kf->x;
}

int main() {
    // 创建并初始化卡尔曼滤波器
    KalmanFilter kf;
    KalmanFilter_Init(&kf, 0.1, 0.1, 0.0);

    // 模拟测量数据
    float measurements[10] = {1.0, 2.0, 3.0, 2.5, 3.5, 3.0, 4.0, 5.0, 4.5, 5.5};

    // 使用卡尔曼滤波器处理测量数据
    for (int i = 0; i < 10; i++) {
        float estimate = KalmanFilter_Update(&kf, measurements[i]);
        printf("Measurement: %f, Estimate: %f\n", measurements[i], estimate);
    }

    return 0;
}
~~~



### 一.控制算法

1. **PID 控制**
   - **描述**：比例-积分-微分控制器（PID）是最常见的控制算法之一，广泛应用于温度控制、速度控制等。
   - **实现**：通过调整比例、积分和微分系数来优化系统响应。
2. **模糊控制**
   - **描述**：基于模糊逻辑的控制方法，适用于不确定性较高的系统。
   - **实现**：使用模糊规则和推理机制来进行控制决策。
3. **状态空间控制**
   - **描述**：通过状态空间模型描述系统动态，适用于多输入多输出（MIMO）系统。
   - **实现**：使用状态反馈和观测器设计来控制系统。
4. **自适应控制**
   - **描述**：能够根据系统的变化自动调整控制参数。
   - **实现**：使用算法（如模型参考自适应控制）来实时更新控制参数。
5. **滑模控制**
   - **描述**：一种鲁棒控制方法，适用于非线性系统。
   - **实现**：通过设计滑模面和控制律来实现系统的跟踪和稳定。
6. **最优控制**
   - **描述**：通过优化某个性能指标（如最小能耗、最小时间）来设计控制策略。
   - **实现**：常用的算法包括线性二次调节器（LQR）。

### 二.滤波算法

1. **卡尔曼滤波**

   - **描述**：一种基于状态空间模型的滤波算法，能够估计系统状态并减小噪声影响。
   - **实现**：适用于线性系统和高斯噪声，常用于导航和定位。

2. **互补滤波**

   - **描述**：结合高通和低通滤波器，常用于传感器融合（如 IMU 数据融合）。
   - **实现**：通过加权平均来平衡短期和长期信号。

3. **数字滤波器**

   - FIR（有限冲击响应）滤波器

     - **描述**：一种常见的数字滤波器，具有线性相位特性。

     - **实现**：通过设计适当的系数来实现低通、高通、带通等滤波。

       ~~~c
       // 带通滤波算法的实现
       #define NUM_TAPS 32 // 滤波器系数的数量
       float32_t firCoeffs[NUM_TAPS] = {
           // 这里填入您的 FIR 系数
         -0.0067905,  -0.00810914, -0.01080181, -0.01440566, -0.01790443, -0.0198824,
        -0.01879344, -0.01329515, -0.00258022,  0.01336665,  0.03364645,  0.05649336,
         0.07949347,  0.09994131,  0.11527114,  0.12348308,  0.12348308,  0.11527114,
         0.09994131,  0.07949347,  0.05649336,  0.03364645,  0.01336665, -0.00258022,
        -0.01329515, -0.01879344, -0.0198824 , -0.01790443, -0.01440566, -0.01080181,
        -0.00810914, -0.0067905
       };
       float32_t firState[NUM_TAPS + 1]; // 状态缓冲区
       float32_t firInput[1024]; // 输入信号
       float32_t firOutput[1024]; // 输出信号
       // FIR 滤波器实例
       arm_fir_instance_f32 firInstance;
       void test_fir(){
           // 模拟输入
           arm_fir_init_f32(&firInstance, NUM_TAPS, firCoeffs, firState, 0);
           for (int i = 0; i < 1024; i++) {
               // 生成 10 Hz 正弦波和 100 Hz 余弦波
               firInput[i] =  ((10*arm_sin_f32(2.0f * PI * 40.0f * i / 1024.0f)) + arm_cos_f32(2.0f * PI * 10.0f  * i / 1024.0f));
               printf("firInput:%f\n",firInput[i]);
               arm_fir_f32(&firInstance, &firInput[i], &firOutput[i], 1);
           }
           for (int i = 0; i < 1024; i++) {
               printf("firOutput:%f\n",firOutput[i]);
           }
       }
       ~~~

       ~~~python
       #用python生成滤波阶数和FIR系数
       from scipy.signal import firwin
       
       # 设计带通滤波器
       num_taps = 32  # 滤波器系数数量
       # 假设您的采样频率为 1000 Hz，那么奈奎斯特频率为 500 Hz。以下是一些频率的归一化示例：
       # 100 Hz 的归一化频率 = 100 / 500 = 0.2
       lowcut = 20 / (1024/2)   # 通带下限（归一化频率=频率/（采样率/2）)
       highcut = 50 / (1024/2)  # 通带上限（归一化频率=频率/（采样率/2）)
       
       # 计算 FIR 系数
       fir_coeffs = firwin(num_taps, [lowcut, highcut], pass_zero=False)
       
       print(fir_coeffs)
       ~~~

       

   - IIR（无限冲击响应）滤波器

     - **描述**：具有反馈结构的数字滤波器，能够实现更高的滤波性能。
     - **实现**：通过设计适当的递归系数来实现滤波。

4. **中值滤波**

   - **描述**：一种非线性滤波方法，能够有效去除脉冲噪声。
   - **实现**：通过取窗口内数据的中值来平滑信号。

5. **自适应滤波**

   - **描述**：根据输入信号的特性动态调整滤波器参数。
   - **实现**：常用的算法包括 LMS（最小均方）和 RLS（递归最小二乘）。

