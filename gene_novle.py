# 步骤1: 读取gene_trans_map.txt，创建isoform到基因的映射
isoform_to_gene = {}
with open('gene_trans_map.txt', 'r') as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) == 2:
            # 以isoform作为键，基因作为值
            isoform_to_gene[parts[1]] = parts[0]

# 步骤2: 读取output_with_expressed_percentage.txt，累加表达百分比
gene_to_percentage = {}
with open('output_with_expressed_percentage.txt', 'r') as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) >= 5:
            isoform = parts[0]
            percentage_str = parts[-1]  # 获取最后一列作为百分比字符串
            percentage = float(percentage_str.rstrip('%'))  # 删除末尾的百分号，并转换为浮点数
            # 使用isoform找到对应的基因，如果找不到，则isoform作为其自己的基因
            gene = isoform_to_gene.get(isoform, isoform)
            gene_to_percentage[gene] = gene_to_percentage.get(gene, 0) + percentage

# 步骤3: 输出到新文件
with open('gene_with_total_percentage.txt', 'w') as f:
    for gene, total_percentage in sorted(gene_to_percentage.items()):
        f.write(f"{gene}\t{total_percentage:.2f}%\n")

