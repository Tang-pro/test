# 首先加载gene_trans_map.txt中每个基因的所有isoform
gene_to_all_isoforms = {}
with open("gene_trans_map.txt", "r") as f:
    for line in f:
        parts = line.strip().split()
        gene = parts[0]
        isoform = parts[1]
        if gene not in gene_to_all_isoforms:
            gene_to_all_isoforms[gene] = set()
        gene_to_all_isoforms[gene].add(isoform)

# 接下来，统计ovule_3dpa_filter.txt中每个基因实际表达的isoform数量
gene_to_expressed_isoforms = {}
with open("ovule_3dpa_filter.txt", "r") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) < 4 or not parts[0].startswith("MSTRG"):
            continue
        isoform_id = parts[0]
        gene_id = isoform_id.rsplit('.', 1)[0]
        if gene_id not in gene_to_expressed_isoforms:
            gene_to_expressed_isoforms[gene_id] = set()
        gene_to_expressed_isoforms[gene_id].add(isoform_id)

# 现在计算每个isoform在其基因中的占比，并输出到新文件中
with open("ovule_3dpa_filter.txt", "r") as infile, open("output_with_expressed_percentage.txt", "w") as outfile:
    for line in infile:
        parts = line.strip().split()
        if len(parts) < 4:
            # 可以选择输出标题行，如果它存在
            outfile.write(line.strip() + "\n")
            continue
        isoform_id = parts[0]
        gene_id = isoform_id.rsplit('.', 1)[0]
        
        # 确认isoform_id是从gene_trans_map.txt中统计的MSTRG开始的isoform
        if gene_id in gene_to_all_isoforms and isoform_id in gene_to_all_isoforms[gene_id]:
            # 使用gene_id获取实际表达的isoform的数量
            expressed_count = len(gene_to_expressed_isoforms.get(gene_id, []))
            total_count = len(gene_to_all_isoforms[gene_id])
            percentage = 100.0 / total_count if expressed_count > 0 else 0
            outfile.write(line.strip() + f"\t{percentage:.2f}%\n")
        else:
            # 如果isoform没有在ovule_3dpa_filter.txt中表达或者不是MSTRG开始的，占比为0%
            outfile.write(line.strip() + "\t0.00%\n")

