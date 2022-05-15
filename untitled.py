import time

from flask import Flask, render_template, request, session, jsonify, send_file
from dbconnection import Db

app = Flask(__name__)
app.secret_key="hiii"
staticpath="C:\\Users\\hp\\PycharmProjects\\untitled\\static\\"


@app.route('/')
def login():
    return render_template("login_temp.html")

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



@app.route('/generate_qr/<om_id>')
def generate_qr(om_id):

    db = Db()
    res = db.selectOne("SELECT lid FROM `orderrmain` WHERE omid = '"+str(om_id)+"'")
    res1 = db.selectOne("SELECT imei FROM `registration` WHERE lid = '"+str(res['lid'])+"'")
    print(res1['imei'])



    a=[0,0,0,1,0,0,2,0,0,0,4,0,0,0,0,3]
    import random
    random.shuffle(a)
    s=""
    for i in a:
        s=s+str(i)+"#"
    # from af import AESCipher
    # aes = AESCipher("0012121212121221", 32)
    #
    # encryp_msg = aes.encrypt(s)
    encryp_msg = s
    #
    # # print(encryp_msg)
    # # msg = aes.decrypt(encryp_msg)
    # # print(msg)
    #
    #
    import qrcode
    img = qrcode.make(res1['imei']+"$"+encryp_msg)
    type(img)  # qrcode.image.pil.PilImage
    img.save("C:\\Users\\hp\\PycharmProjects\\untitled\\static\\qr.png")
    # return "ok"
    return render_template('admin/view_qr.html',a=a)

    # filename = "C:\\Users\\hp\\PycharmProjects\\untitled\\static\\qr.png"
    # return send_file(filename, mimetype='image/png')









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

# ----------------------------------Android-------

@app.route("/and_login_post",methods=['POST'])
def and_login_post():
    d=Db()

    username=request.form['uname']
    password=request.form['psw']
    qry = "SELECT * FROM `login` WHERE `username`='" + username + "' AND `password`='" + password + "'"
    res=d.selectOne(qry)
    print(res['lid'])
    if res is not None:
        if res["type"]=="user":
            return jsonify(status="ok",lid=res["lid"])
        else:
            return jsonify(status="no")
    else:
        return jsonify(status="no")


@app.route("/and_signup",methods=['POST'])
def and_signup():
    d=Db()
    use = request.form['name']
    place = request.form['place']
    pin = request.form['pin']
    post = request.form['post']
    phone = request.form['phone']
    email = request.form['email']
    password=request.form['password']
    image = request.form['photo']
    imei = request.form['imei']
    import base64

    timestr = time.strftime("%Y%m%d-%H%M%S")
    print(timestr)
    a = base64.b64decode(image)
    fh = open("C:\\Users\hp\\PycharmProjects\\untitled\\static\\userimg\\" + timestr + ".jpg", "wb")
    path = "/static/userimg/" + timestr + ".jpg"
    fh.write(a)
    fh.close()

    qry="INSERT INTO  `login` (`username`,`password`,`type`) VALUES('"+use+"','"+password+"','user')"
    db=Db()
    lid=str(db.insert(qry))


    qry="INSERT INTO `registration`(lid,name,place,pin,post,phoneno,email,image,imei)VALUES('"+lid+"','"+use+"','"+place+"','"+pin+"','"+post+"','"+phone+"','"+email+"','"+path+"','"+imei+"')"
    res=d.insert(qry)
    return  jsonify(status="ok")

@app.route("/and_productview",methods=['POST'])
def and_productview():
    d=Db()

    catid=request.form['catid']
    qry="SELECT `product`.*,category.* FROM `category` INNER JOIN `product` ON  `category`.catid=`product`.`catid` WHERE  category.catid='"+catid+"'"
    res=d.select(qry)
    return jsonify(status="ok",users=res)


@app.route("/categoryview",methods=['POST'])
def categoryview():
    d=Db()
    qry="SELECT * from category"
    res=d.select(qry)
    return jsonify(status="ok",users=res)


@app.route("/and_cartview",methods=['POST'])
def and_cartview():
    d=Db()
    lid=request.form['lid']
    qry="SELECT `cart`.*,`product`.*,category.* FROM `product` INNER  JOIN cart ON `product`.`productid`=`cart`.`productid` INNER JOIN category ON product.catid=category.catid  WHERE  lid='"+lid+"'"
    res=d.select(qry)
    print(qry)
    print(res)
    tot = d.selectOne("SELECT SUM(cart.`quantity`*`product`.`price`) as total FROM `cart`,`product` WHERE cart.`productid`=product.`productid` AND `cart`.`lid`='" + str(lid) + "'")
    print(tot['total'])

    # qr = "DELETE FROM `cart` WHERE `cartid`='" + lid + "'"
    # res = d.delete(qr)
    return jsonify(status="ok",users=res,total = tot['total'])

@app.route("/and_purchasehistory",methods=['POST'])
def and_purchasehistory():
    d=Db()
    lid=request.form['lid']
    qry="SELECT * FROM `orderrmain` where omid='"+lid+"'"
    res=d.select(qry)
    print(qry)
    return  jsonify(status="ok",users=res)




@app.route("/and_profileview",methods=['POST'])
def and_profileview():
    lid=request.form['lid']
    d=Db()
    qry="SELECT * FROM `registration` WHERE lid='"+lid+"'"
    res=d.selectOne(qry)
    print(qry)
    print(res)
    return  jsonify(status="ok",name=res["name"],place=res["place"],pin=res["pin"],post=res["post"],phoneNo=res["phoneno"],email=res["email"],image=res["image"])
@app.route("/add_cartadd",methods=['POST'])
def add_cartadd():
    c=request.form['lid']
    p=request.form['pid']
    qty=request.form['qty']
    pri=request.form['price']
    # c1=request.form['cartid']
    d=Db()
    qry="INSERT INTO `cart`(`productid`,`quantity`,`lid`)VALUES('"+p+"','"+qty+"','"+c+"')"
    res =d.insert(qry)

    return jsonify(status="ok")



@app.route("/and_enter_details",methods=['POST'])
def and_enter_details():
    place=request.form['place']
    pin=request.form['pin']
    post=request.form['post']
    district=request.form['district']
    lid=request.form['lid']
    tot=request.form['tot']

    print(place)
    db =Db()
    omid=db.insert("insert into `orderrmain`(`lid`,`totalamt`,`date`,`place`,`pin`,`post`,`district`) VALUES ('"+lid+"','"+str(tot)+"',curdate(),'"+place+"','"+pin+"','"+post+"','"+district+"')")
    res = db.select("select * from `cart` WHERE `lid`='"+str(lid)+"'")
    print(res)
    for i in res:
        db.insert("INSERT INTO ordersub (`omid`,`productid`,`os_quantity`) values('"+str(omid)+"','"+str(i['productid'])+"','"+str(i['quantity'])+"')")
        return jsonify(status="ok")
    # c1=request.form['cartid']
    # d=Db()
    # qry="INSERT INTO `cart`(`productid`,`quantity`,`lid`)VALUES('"+p+"','"+qty+"','"+c+"')"
    # res =d.insert(qry)

    return jsonify(status="ok")
@app.route("/remove_cart",methods=['POST'])
def remove_cart():
    lid=request.form['lid']
    cartid=request.form['cartid']
    db =Db()
    db.delete("delete from cart where cartid = '"+str(cartid)+"' ")
    return jsonify(status="ok")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
