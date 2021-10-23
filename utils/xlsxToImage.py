import xlrd
import xlwt
import os
import urllib.request

urls_Img=[]
itemNames=[]
file_kinds=[]
folder_path="D:\\DataSets\\old-sword\\luyiTest2\\"

def handle_excel(excel_name):
    workbook = xlrd.open_workbook(excel_name)
    allSheetNames = workbook.sheet_names()
    # print(allSheetNames)#获取sheet，list保存

    sheet_name = workbook.sheet_names()[0] #可更改索引
    # print(sheet_name)

    sheet_content=workbook.sheet_by_index(0)
    # print(sheet_content.name,sheet_content.nrows,sheet_content.ncols)#获取sheet名，行数，列数

    rows_title=sheet_content.row_values(0)#索引从0开始，list保存
    cols_itemName=sheet_content.col_values(8)
    cols_ImgPath=sheet_content.col_values(6)

    itemNames.extend(cols_itemName)
    urls_Img.extend(cols_ImgPath)
    file_kinds.extend(rows_title)

    for url in urls_Img[1:]:
        index=urls_Img.index(url)
        Img_name=itemNames[index]#用以保存的图片名
        itemInfo=sheet_content.row_values(index)

        file_path= folder_path +file_kinds[4] #修改此处即可放入不同文件夹
        file_location=file_path + "\\" + itemInfo[4] #与上步同步修改
        # print(file_location)
        try:
            if not os.path.exists(file_location):
                os.makedirs(file_location)
            file_suffix = os.path.splitext(url)[1]  # 获取后缀
            filename = file_location + "\\" + Img_name + file_suffix
            print(filename)
            urllib.request.urlretrieve(url, filename=filename)
        except IOError as e:
            print(1,e)
        except Exception as e:
            print(2,e)
    print("---------------complete--------------")

# if __name__ == '__main__':
#     handle_excel("Luyisengling2.xlsx")