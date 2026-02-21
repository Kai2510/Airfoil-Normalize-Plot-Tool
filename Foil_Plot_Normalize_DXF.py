import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import ezdxf
in_name="TL54.dat"#输入文件名
out_name="TL54_Normalized.dat"#输出文件名
dxf_name="TL54.dxf"
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


scale = 100.0  # mm
points_scaled = data_out.values * scale
doc = ezdxf.new('R2004')  # DXF 2004
msp = doc.modelspace()

# 检查翼型是否封闭（首尾点距离很小）
first_point = points_scaled[0]
last_point = points_scaled[-1]
distance = np.sqrt((last_point[0] - first_point[0])**2 + (last_point[1] - first_point[1])**2)
is_closed = distance < 0.1  # Tolerance of closed
print(f"Distance between : {distance:.4f}mm, Closed?: {is_closed}")

# Try spline
try:
    # ezdxf v0.17+
    spline = msp.add_spline(
        fit_points=points_scaled.tolist(),
        degree=3
    )
    if is_closed:
        spline.dxf.closed = True

    print("Spline successful")

except TypeError as e:
    print(f"Spline failed: {e}")

    # 方法2：备用方案 - 使用多段线（如果样条线失败）
    print("Polyline")
    msp.add_lwpolyline(
        points=points_scaled.tolist(),
        close=is_closed
    )
doc.saveas(dxf_name)
print(f"  Points: {len(points_scaled)}")
print(f"  Closed: {'Y' if is_closed else 'N'}")
print(f"  Format: DXF 2004")
