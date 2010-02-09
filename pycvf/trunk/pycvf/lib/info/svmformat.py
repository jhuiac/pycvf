def output_matrix_svmformat(matrix,filename):
    f=file(filename,"w")
    for y in range(matrix.shape[0]):            
        f.write(" ".join( (map(lambda x,y:"%d:%f"%(x,y),range(1,1+matrix.shape[1]),matrix[y,:].flat))))
        f.write("\n")
    f.close()

    
def output_matrix_svmformat_with_labels(matrix,labels,filename):
    f=file(filename,"w")
    il=iter(labels)
    for y in range(matrix.shape[0]):
        f.write("%d "%(il.next()))
        f.write(" ".join( (map(lambda x,y:"%d:%d"%(x,y),range(matrix.shape[1]),matrix[y,:].flat))))
        f.write("\n")
    f.close()
    