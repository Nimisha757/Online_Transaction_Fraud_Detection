from flask import Flask, render_template, request, session
from dbconnection import Db

app = Flask(__name__)
app.secret_key="hiii"
staticpath="C:\\Users\\hp\\PycharmProjects\\untitled\\static\\"


@app.route('/')
def login():
    return render_template("login.html")

@app.route('/login_post',methods=['post'])
def login_post():

        us=request.form['textfield']
        ps=request.form['textfield2']
        qry="SELECT * FROM `login` WHERE `username`='"+us+"' AND `password`='"+ps+"'"
        d=Db()
        res= d.selectOne(qry)
        if res!='':
            session['l_id']=res['lid']
            type=res['type']

            if type=='admin':
                return '''<script>alert('success');window.location='/adminhome'</script>'''

            else:
                return '''<script>alert('invalid');window.location='/login'</script>'''
        else:
            return '''<script>alert('invalid');window.location='/login'</script>'''



@app.route('/adminhome')
def adminhome():
       return render_template("admin/adminhome.html")

@app.route('/add_category')
def add_category():
    return render_template("admin/CATEGORY (ADD).html")
@app.route('/add_category_post',methods=['post'])
def add_category_post():

    cat2=request.form['cat']
    print(cat2)
    qry="INSERT INTO `category`(`catname`)VALUES('"+cat2+"')"
    d=Db()
    d.insert(qry)
    return '''<script>alert('success');window.location='/add_category'</script>'''



@app.route('/viewcategory')
def viewcate():
        d=Db()
        qry="SELECT * FROM `category`"
        res=d.select(qry)

        return render_template("admin/view category.html",data=res)

@app.route('/viewcat_post',methods=['post'])
def viewcat_post():
        cat=request.form['textfield']
        D=Db()
        qry="SELECT * FROM `category` WHERE `catname` LIKE '%"+cat+"%'"
        res=D.select(qry)
        return render_template("admin/view category.html",data=res)
@app.route('/deletecategory/<cid>')
def deletecategory(cid):
    d=Db( )
    qry="DELETE FROM category where category.catid='"+cid+"'"
    res=d.delete(qry)
    return "<script>alert('Deleted Successfully');window.location='/viewcategory'</script>"
@app.route('/editcategory/<eid>')
def editcategory(eid):
    d=Db()
    qry="SELECT * FROM `category` WHERE catid='"+eid+"'"
    res=d.selectOne(qry)

    return render_template('admin/Editcategory.html',data=res)
@app.route('/editcategory_post',methods=['post'])
def editcategory_post():
    c=request.form['cat']
    c_id=request.form['c_id']
    d=Db()
    qry="UPDATE `category` SET catname='"+c+"' WHERE catid='"+c_id+"'"
    res=d.update(qry)
    return '''<script>alert("Updated Successfully");window.location='/viewcategory'</script>'''




@app.route('/add_product')
def add_product():
    qry="SELECT * FROM `category`"
    d=Db()
    res=d.select(qry)

    return render_template("admin/PRODUCT(ADD).html",cat=res)


@app.route('/product_add_post',methods=['post'])
def product_add_post():

        cat=request.form['cat3']
        p=request.form['textfield2']
        pri=request.form['textfield3']
        im=request.files['fileField']
        im.save(staticpath+"product\\"+im.filename)
        path="/static/product/"+im.filename

        qry="INSERT INTO `product`(`catid`,`productname`,`price`,`pimage`)VALUES('"+cat+"','"+p+"','"+pri+"','"+path+"')"
        d=Db()
        d.insert(qry)

        print(cat,p)
        return '''<script>alert('success');window.location='/add_product'</script>'''
@app.route('/viewproduct')
def viewproduct():
    d = Db()
    qry = " SELECT `product`.*,category.* FROM `category` INNER JOIN `product` ON  `category`.catid=`product`.`catid`"

    res = d.select(qry)
    return render_template("admin/view product.html", data=res)



@app.route('/viewproduct_post',methods=['post'])
def viewprod_post():

        p1=request.form['textfield']
        d=Db()
        qry="SELECT `product`.*,category.* FROM `category` INNER JOIN `product` ON  `category`.catid=`product`.`catid` WHERE productname LIKE '%"+p1+"%'"
        res = d.select(qry)
        return render_template("admin/view product.html", data=res)
@app.route('/deleteproduct/<pid>')
def deleteproduct(pid):
    d=Db()
    qry="DELETE FROM product WHERE product.productid='"+pid+"'"
    res=d.delete(qry)
    return '''<script>alert("Deleted Successfully");window.location='/viewproduct'</script>'''
@app.route('/editproduct/<epid>')
def editproduct(epid):
    d=Db()

    qry="SELECT `product`.*,category.* FROM `category` INNER JOIN `product` ON  `category`.catid=`product`.catid WHERE productid='"+epid+"'"
    res=d.selectOne(qry)

    qry1 = "SELECT * FROM `category`"

    res1 = d.select(qry1)

    return render_template('admin/Editproduct.html',data=res,cat=res1)
@app.route('/editproduct_post',methods=["post"])
def editproduct_post():
    cat4 = request.form['cat3']
    p4 = request.form['textfield2']
    pri4 = request.form['textfield3']
    po_id = request.form['po_id']
    d = Db()
    if 'fileField' in request.files:

        im4 = request.files['fileField']
        if im4.filename!='':
            im4.save(staticpath + "product\\" + im4.filename)
            path = "/static/product/" + im4.filename
            qry = "UPDATE `product` SET catid='" + cat4 + "',productname='"+p4+"',price='"+pri4+"',pimage='"+path+"' WHERE productid='" + po_id + "'"
            res=d.update(qry)
        else:
            qry = "UPDATE `product` SET catid ='" + cat4 + "',productname='" + p4 + "',price='" + pri4 + "' WHERE productid='" + po_id + "'"
            res = d.update(qry)
    else:
        qry = "UPDATE `product` SET catid='" + cat4 + "',productname='" + p4 + "',price='" + pri4 + "' WHERE productid='" + po_id + "'"
        res = d.update(qry)
    return '''<script>alert("Updated Successfully");window.location='/viewproduct'</script>'''






@app.route('/viewordermain')
def viewordermain():
    d=Db()
    qry="SELECT `registration`.`name`,`registration`.`place`,`registration`.`pin`,`registration`.`post`,`registration`.`phoneno`,`registration`.`email`, `orderrmain`.omid,   `orderrmain`.`totalamt`,`orderrmain`.`date`,`orderrmain`.`place`,`orderrmain`.`pin`,`orderrmain`.`post`,`orderrmain`.`district` FROM `orderrmain` INNER JOIN `registration` ON `orderrmain`.lid=`registration`.`lid`"
    res=d.select(qry)
    return render_template("admin/view order main.html",data=res)


@app.route('/ordermain_post',methods=["post"])
def ordermain_post():
    date1=request.form['d1']
    date2=request.form['d2']
    d=Db()

    qry = "SELECT `registration`.`name`,`registration`.`place`,`registration`.`pin`,`registration`.`post`,`registration`.`phoneno`,`registration`.`email`, `orderrmain`.omid,   `orderrmain`.`totalamt`,`orderrmain`.`date`,`orderrmain`.`place`,`orderrmain`.`pin`,`orderrmain`.`post`,`orderrmain`.`district` FROM `orderrmain` INNER JOIN `registration` ON `orderrmain`.lid=`registration`.`lid` where `orderrmain`.`date` BETWEEN '"+date1+"' AND '"+date2+"'"
    res = d.select(qry)
    return render_template("admin/view order main.html", data=res)

@app.route('/viewordersub/<oid>')
def viewordersub(oid):
    d=Db()
    qry="SELECT ordersub.*,`product`.`productname`,`product`.`price`,`product`.`pimage` FROM `ordersub`INNER JOIN `product` ON `ordersub`.`productid`=`product`.`productid` WHERE `ordersub`.`omid`='"+oid+"'"
    res=d.select(qry)

    return render_template("admin/View order Sub.html",data=res)


@app.route('/viewusers')
def viewusers():
    d=Db()
    qry="SELECT * FROM `registration`"
    res=d.select(qry)
    return render_template("admin/View Registered user.html",data=res)


if __name__ == '__main__':
    app.run()
