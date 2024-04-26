from django.shortcuts import render
from django.http import HttpResponse
from .project2 import *
from django.shortcuts import redirect





def dump(btree):
    with open("myApp/main.txt", 'w') as f:
        f.write(str(btree))
        
def dumptree(btree):
    with open("myApp/tree.txt", 'w') as f:
        f.write(str(btree))

def load():
    with open("myApp/main.txt", 'r') as f:
        x = f.read()
        y  = eval(x)
        return y
    
def loadtree():
    with open("myApp/tree.txt", 'r') as f:
        x = f.read()
        y  = eval(x)
        return y

def random(request):
    return render(request, "index.html")


def all_emp(request):
    context = {}
    # emps = inorder_traversal(EMP_DATA)
    emps = load()
    context = {"emps": emps}
    return render(request, "all_emp.html", context)


def add_emp(request):
    if request.method == "POST":
        #getting data from form
        btree = loadtree()
        ID1 = request.POST["id"]
        first_name = request.POST["first_name"]
        salary = request.POST["salary"]
        Birthday = request.POST["birthday"]
        Position = request.POST["position"]
        Email = request.POST["email"]
        Address = request.POST["address"]

        employee = {
            "id": str(ID1),
            "name": first_name,
            "salary": salary,
            "dob": Birthday,
            "position": Position,
            "email": Email,
            "address": Address,
        }
        insert_b_tree(btree, ID1, employee)
        
        x = inorder_traversal(btree)
        dump(x)
        dumptree(btree)
        
        return redirect('all_emp')

    elif request.method == "GET":
        return render(request, "add_emp.html")
    else:
        return HttpResponse("An Exception ocurred")


def remove_emp(request):
    if request.method == "POST":
        # get data
        btree = loadtree()
        ID1 = request.POST["id"]
        #delete from tree
        delete_b_tree(btree, btree['root'], ID1)    
        x = inorder_traversal(btree)
        dump(x)
        dumptree(btree)
        
        #sending data to HTML file
        return redirect('all_emp')

    elif request.method == "GET":
        return render(request, "remove_emp.html")
    else:
        return HttpResponse("An Exception occurred")


def change_emp(request):
    if request.method == "POST":
        ID1 = request.POST["id"]
        # get data
        d = loadtree()
        emps = search_b_tree(d, ID1)
        # if search return none render  empty data on html file
        
        if emps == None:
            emps = [
                (
                    "",
                    {
                        "id": "",
                        "name": "",
                        "dob": "",
                        "address": "",
                        "email": "",
                        "position": "",
                        "salary": "",
                    },
                )
            ]
        else:
            emps = [(ID1, emps[1])]
        context = {"emps": emps}
        return render(request, "all_emp.html", context)
    elif request.method == "GET":
        return render(request, "change_emp.html")

    else:
        return HttpResponse("Error")


def update_emp(request):
    if request.method == "POST":
        btree = loadtree()
        ID1 = request.POST["id"]
        datatype = request.POST["datatype"]
        data = request.POST["data"]
        # get data from tree
        tr = loadtree()
        emps = search_b_tree(tr, ID1)
        if emps is not None:
            emps[1][datatype] = data
            update(btree, ID1, emps[1])
            
        x = inorder_traversal(btree)
        dump(x)
        dumptree(btree)
        return redirect('all_emp')
        
    elif request.method == "GET":
        return render(request, "update_emp.html")
    
    else:
        return HttpResponse("Error: Invalid request method")




