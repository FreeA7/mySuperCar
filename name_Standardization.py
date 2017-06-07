import os
import re

p = re.compile('[^\\\]+$')
dir = "E:\\BaiduYunDownload"
roots = []
dirs = []
files = []
for root, dirs, files in os.walk(dir):
    if root not in roots:
        # print (root)
        roots.append(root)

roots = sorted(roots, key=lambda x: len(x), reverse=True)

for i in range(len(roots)):
    target = p.search(roots[i]).group()
    root_target = roots[i][:-1 * len(target)]
    if len(re.findall('[^0-9|a-z|A-Z|\u4e00-\u9fa5]', target)) != 0:
        new_target = re.sub('[^0-9|a-z|A-Z|\u4e00-\u9fa5]', '', target)
        os.rename(root_target + target, root_target + new_target)
        # print (root_target + new_target)

print('\'' + dir + '\'' + '下的文件夹名修改成功')

for root, dirs, files in os.walk(dir):
    for file in files:
        name = re.search('^[^.]+', file).group()
        back = file[len(name):]
        if len(re.findall('[^0-9|a-z|A-Z|\u4e00-\u9fa5]', name)) != 0:
            new_name = re.sub('[^0-9|a-z|A-Z|\u4e00-\u9fa5]', '', name)
            new_name = new_name + back
            os.rename(os.path.join(root, file), os.path.join(root, new_name))
            # print (os.path.join(root,new_name))

print('\'' + dir + '\'' + '下的文件名修改成功')

# for root in roots:
# 	if root.find('12'):
# 		new_root = root.replace('12','kkxx')
# 		os.rename(root,new_root)
# 		root = new_root
# 		print (root)

# for file in files:
#     print (os.path.join(root,file))
#     newname = file.replace('39','78')
#     os.rename(os.path.join(root,file),os.path.join(root,newname))

# newroot = file.replace('12','78')
# os.rename(os.path.join(root,file),os.path.join(root,newname))
