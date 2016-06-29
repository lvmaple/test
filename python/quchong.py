fp1 = open("22")
fp2 = open("22_r", "w+")
list_t = []
for line in fp1:
    list_t.append(str(line))
list_r = list(set(list_t))
list_r.sort()
lits_rt = "".join(list_r)
# for list_rt in list_r:
    # fp2.write(list_rt)
fp2.write(lits_rt)
fp1.close()
fp2.close()
