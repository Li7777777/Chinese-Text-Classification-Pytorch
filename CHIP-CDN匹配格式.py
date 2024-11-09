import json
import os

errText = ''

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data




if __name__ == '__main__':
    dataSet = 'CHIP-CDN'
    data_path = f'./{dataSet}/data/'
    class_path = f'{data_path}/class.txt'
    train_path = f'{data_path}/train.txt'
    dev_path = f'{data_path}/dev.txt'
    test_path = f'{data_path}/test.txt'

    # 构建class文件

    # class_set = []
    # with open(data_path+'cName_idc10.json', 'r', encoding='utf-8') as f:
    #     data_cName_idc10 = json.load(f)
    # for vs in data_cName_idc10.values():
    #     for v in vs:
    #         class_set.append(v)
    # text = ''
    # with open(class_path, 'w', encoding='utf-8') as f:
    #     for c in class_set:
    #         text += c+'\n'
    #     text = text.strip()
    #     f.write(text)
    # print(f'class文件构建完成，共{len(class_set)}个类别')

    # 构建class为tarin所有的
    class_set_all = []
    with open(data_path+'cName_idc10.json', 'r', encoding='utf-8') as f:
        data_cName_idc10 = json.load(f)
    for vs in data_cName_idc10.values():
        for v in vs:
            class_set_all.append(v)
    class_set = []
    # ======================================================================
    index_class = []

    for file in os.listdir(data_path):
        if file.endswith('.json'):
            if file.startswith('CHIP-CDN_'):
                if file.endswith('test.json'):
                    continue
                file_path = os.path.join(data_path, file)
                data = load_json(file_path)
                outText = ''
                for item in data:
                    for k in item['normalized_result'].split('##'):
                        try:
                            for icd in data_cName_idc10[k]:
                                # 过滤掉训练集没有的标签
                                if icd not in class_set:
                                    class_set.append(icd)
                                outText += item['text']+'\t'+str(class_set.index(icd))+'\n'
                        except KeyError:
                            errText += str(item) + '\n'
                outText = outText.strip()
                if file.endswith('dev.json'):
                    # 保存前一半数据作为测试集，后一半数据作为验证集
                    outList = outText.split('\n')
                    num = len(outList)
                    dev_num = num // 2
                    dev_text = '\n'.join(outList[:dev_num])
                    test_text = '\n'.join(outList[dev_num:])
                    with open(dev_path, 'w', encoding='utf-8') as f:
                        f.write(dev_text)
                    with open(test_path, 'w', encoding='utf-8') as f:
                        f.write(test_text)
                elif file.endswith('train.json'):
                    with open(train_path, 'w', encoding='utf-8') as f:
                        f.write(outText)
    # 输出class文件，只包含训练集的标签
    text = ''
    with open(class_path, 'w', encoding='utf-8') as f:
        for c in class_set:
            text += c+'\n'
        text = text.strip()
        f.write(text)
    print(f'class文件构建完成，共{len(class_set)}个类别')
    
    print(f'数据集{dataSet}构建完成')

    if errText:
        with open(f'./{dataSet}/err.txt', 'w', encoding='utf-8') as f:
            f.write(errText)