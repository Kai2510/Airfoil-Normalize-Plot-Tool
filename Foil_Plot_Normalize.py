import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
in_name="TL54m1.dat"#输入文件名
out_name="TL54m1_Normalized.dat"#输出文件名
data_in=pd.read_csv(in_name,delimiter='\s+',index_col=False,header=None,skiprows=1);
#这里分隔符是任意多空白字符，包括空格、制表符、换页符
data_in=data_in.iloc[:,0:2]
#Normalize the foil - rotate
angle_to_rot = math.atan(data_in.iloc[-1,1]/data_in.iloc[-1,0])
M_rot=np.array([[math.cos(angle_to_rot),-math.sin(angle_to_rot)],
                [math.sin(angle_to_rot),math.cos(angle_to_rot)]     ])
for i in range(len(data_in.iloc[:,0])):
    data_in.iloc[i,0]=np.matmul(data_in.iloc[i,0:2],M_rot)[0]
    data_in.iloc[i,1]=np.matmul(data_in.iloc[i,0:2],M_rot)[1]
#Normalize the foil - scale x-axis
X_scale_factor=1/data_in.iloc[0,0]
for i in range(len(data_in.iloc[:,0])):
    data_in.iloc[i,0]=data_in.iloc[i,0]*X_scale_factor;
#Plot
plt.plot(data_in.iloc[:,0],data_in.iloc[:,1])
plt.axis('scaled')  # Either of these settings is ok.
# plt.axis('equal')
plt.show()
#Output
data_out = data_in.iloc[:,0:2]
data_out.columns=[in_name,' ']
data_out.to_csv(out_name,sep='\t',index=False,float_format='%.6e');
