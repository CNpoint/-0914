# -*- coding: utf-8 -*-
# @Project_Name: draw 
# File_Name: 3D_Cloud_draw 
# @Author: -SGF- 
# @Time: 2022-09-14 
# @IDE_Name: PyCharm

import matplotlib as mpl
import os
from tqdm import tqdm
import pygrib as pg
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as clr
import cartopy.crs as ccrs
import cartopy.io.shapereader
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter


def Draw(extent, root, draw_value, shp_file, file_name, out_path):
    print('绘制该文件夹下文件：', root)
    print('绘制文件名：', file_name)
    grbs = pg.open(root + '/' + file_name)
    out_file = file_name[14:28]
    grbs.seek(0)  # 指定指针
    for grb in grbs:  # 看看里面有几组数据
        print(grb)  # 然后得出绘图name
    # 选择并提取出对应的变量名称
    grb = grbs.select(name=draw_value)[0]
    # grb = grbs.message(2) # get the second grib message

    # 获取经纬度信息
    lat, lon = grb.latlons()
    # print(grb.keys())

    # 定义轴线范围
    # box = extent
    box = [lon.min(), lon.max(), lat.min(), lat.max()]
    values = grb.values

    fig = plt.figure(figsize=[14, 12], dpi=200)  # 像素大小

    ax = plt.axes(projection=ccrs.PlateCarree())

    # cmap = clr.ListedColormap(["#00ECEC", "#00D800",
    #                            "#019000", "#FFFF00", "#E7C000",
    #                            "#FF9000", "#FF0000", "#D60000",
    #                            "#C00000", "#FF00F0", "#9650B4"
    #                            ])  # 色标
    # cmap.set_over((0.001462, 0.000466, 0.013866, 1))  # 图例
    # cmap.set_under((1, 1, 1, 0))
    # color_lev = np.array([15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70])  # 色标等级
    cmap = clr.ListedColormap(["#928246", "#847746",
                               "#747474", "#ADB7B6", "#D5D5CD"
                               ])  # 色标
    cmap.set_over((0.001462, 0.000466, 0.013866, 1))  # 图例
    cmap.set_under((1, 1, 1, 0))
    color_lev = np.array([0, 9.9, 29.9, 79.9, 99.9, 100])  # 色标等级

    norm = mpl.colors.BoundaryNorm(color_lev, cmap.N)
    ax.background_patch.set_visible(False)
    ax.outline_patch.set_visible(True)  # 开启GeoAxes框线

    # 绘制等高线，填充等高线
    filled_c = ax.contourf(lon, lat, values, transform=ccrs.PlateCarree(),
                           cmap=cmap, levels=color_lev, norm=norm)
    # Use the line contours to place contour labels.
    fig.colorbar(filled_c)

    reader = cartopy.io.shapereader.Reader(shp_file)
    geometries = reader.geometries()
    ax.add_geometries(geometries, crs=ccrs.PlateCarree(),
                      linestyle='-',
                      facecolor='none',
                      edgecolor='black', linewidth=0.5)

    # 标题
    fig.text(0.335, 0.9, "{}-{}".format('Cloud cover_', out_file), color='black', fontsize=16)
    ax.set_extent(box)

    """
    绘制坐标轴
    """
    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.yaxis.set_major_formatter(LatitudeFormatter())
    ax.set_xticks(
        np.round(np.arange(extent[0], extent[1], 2), 2),
        crs=ccrs.PlateCarree())  # x轴
    ax.set_yticks(
        np.round(np.arange(extent[2], extent[3], 2), 2),
        crs=ccrs.PlateCarree())  # y轴
    ax.spines['geo'].set_visible(False)
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_visible(True)
    plt.tick_params(labelsize=14)

    # 指定图片保存路径
    figure_save_path = out_path

    if not os.path.exists(figure_save_path):
        os.makedirs(figure_save_path)  # 如果不存在目录figure_save_path，则创建
    plt.savefig(os.path.join(figure_save_path, out_file + '_3D_Cloud.png'))  # 第一个是指存储路径，第二个是图片名字
    print('绘制成功：', out_file + '_3D_Cloud.png')

    # plt.show()


def file_list(path):
    for root, dirs, files in os.walk(path):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        # 遍历文件
        list1 = []
        for f in files:
            list1.append(f)

        return root, list1

        # 遍历所有的文件夹
        # for d in dirs:
        #     print(os.path.join(root, d))


if __name__ == '__main__':
    extent = [95.00, 108.65, 18.60, 31.70]  # 云南轴线范围
    # extent = [80.00, 120.00, 5.00, 110.00]  # 中国轴线范围
    path_file = r'data/20220912_3DCloud'  # 绘制文件地址
    draw_value = 'Cloud cover'  # values元素名称
    shp_file = "shp/China/China.shp"  # 地图边界名
    out_path = r'png/3D_Cloud'  # 图片输出名
    root, list1 = file_list(path_file)
    print(list1)
    for i in tqdm(range(len(list1))):
        Draw(extent, root=root, draw_value=draw_value, shp_file=shp_file, file_name=list1[i], out_path=out_path)
