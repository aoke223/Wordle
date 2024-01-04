from printTest import*
def binarySearch(item: str, alist:list[str]) -> bool:
    low= 0
    high= len(alist)-1
    while low<= high:
        mid=(low+high)//2
        if alist[mid] == item:
            return True
        elif alist[mid] > item:
            high = mid -1
        else:
            low = mid + 1
    return False
        
def mergeSort(alist: list[str]) -> list[str]:
    if len(alist) <= 1:
        return alist
    mid=len(alist) // 2 
    blist= alist[:mid]
    clist= alist[mid:]
    blist= mergeSort(blist)
    clist=mergeSort(clist)
    return merge(blist, clist)



def merge(blist:list[str], clist:list[str]) -> list[str]:
    final=[]
    i=0; j=0
    while i < len(blist) and j <len(clist):
        if blist[i] < clist[j]:
            final.append(blist[i])
            i+=1
        else:
            final.append(clist[j])
            j+=1
    final += blist[i:]
    final += clist[j:]
    return final



def main() -> None:
    item="bow"
    alist= ["bow", "cow","dow", "how", "kow", "low", "pow", "row", "sow", "xow"]
    printTest(binarySearch, item, alist, expected=True)
    item="go"
    alist=["engines","go","ready","set","start"]
    printTest(binarySearch, item, alist, expected=True)
    item="bad"
    alist=[]
    printTest(binarySearch, item, alist, expected=False)
    item="lead"
    alist=["bread","cream", "lead","lean","steam","peen"]
    printTest(binarySearch, item, alist, expected=True)
    item="Kobe"
    alist=["Jordan","Kyrie","Lebron", "Shaq","Wilt"]
    printTest(binarySearch, item, alist, expected=False)
    blist=["jordan","kyrie","lebron", "shaq","wilt"]
    clist=["engines","go","ready","set","start"]
    printTest(merge, blist, clist, expected=['engines', 'go', 'jordan', 'kyrie', 'lebron', 'ready', 'set', 'shaq', 'start', 'wilt'])
    blist=[]
    clist=[]
    printTest(merge, blist, clist, expected=[])
    blist=["it", "Will"]
    clist=["merge!"]
    printTest(merge, blist, clist, expected=["it", "Will", "merge!"])
    blist=["die", "young"]
    clist=[]
    printTest(merge, blist, clist, expected=["die", "young"])
    blist=[]
    clist=["die", "young"]
    printTest(merge, blist, clist, expected=["die", "young"])
    blist=["america", "china", "dutch", "iran"]
    clist=["nigeria", "mumbai", "poland"]
    printTest(merge, blist, clist, expected=["america", "china", "dutch", "iran", "nigeria", "mumbai", "poland"])
    blist=["church"]
    clist=[]
    printTest(merge, blist, clist, expected=["church"])
    blist=["best"]
    clist=["there", "is"]
    printTest(merge, blist, clist, expected=["best", "there", "is"])
    alist=["start", "your", "engines", "racers","ready", "set", "go"]
    printTest(mergeSort, alist, expected=["engines","go","racers", "ready","set","start","your"])
    alist=[]
    printTest(mergeSort, alist, expected=[])
    alist=["goat"]
    printTest(mergeSort, alist, expected=["goat"])
    alist=["nigeria", "mumbai", "poland", "america", "china", "dutch", "iran"]
    printTest(mergeSort, alist, expected=["america", "china", "dutch", "iran", "mumbai", "nigeria", "poland"])
    alist=["is", "it", "possible", "to", "sort", "this"]
    printTest(mergeSort, alist, expected=["is", "it", "possible", "sort", "this", "to"])
    
    

    
if __name__ == "__main__":
    main()

