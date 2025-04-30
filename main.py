##################导入所需的库和模块##################

#Flask:用于创建Flask应用实例
#render_template:用于渲染HTML模板
#request:用于处理HTTP请求
#redirect和url_for:用于重定向指定的路由
#flash:用于在页面上显示一次性的提示消息
#SQLAchemy:Flask的SQL工具包，用于数据库操作
#FlaskForm:用于创建表单类
#StringField,TextAreaField,SubmitField:用于定义表单中不同字段类型
#DataRequired:用于表单字段验证，确保字段不为空
from flask import Flask, flash, redirect, url_for, render_template
#数据库操作
from flask_sqlalchemy import SQLAlchemy
#表单操作
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import DataRequired,Email,Length
from flask_wtf import FlaskForm
from datetime import datetime




##################创建Flask应用实例，配置应用的密钥和数据库链接##################
#创建一个Flask应用实例
app = Flask(__name__)
#设置应用的密钥，用于csrf（跨站请求伪造）保护
app.secret_key = 'your_secret_key_here'
#设置数据库链接URL，这里使用MySql数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/mydb'
#初始化SQLAlchemy并绑定到Flask应用
db=SQLAlchemy(app)

##############定义数据库模型Article##################

#创建一个继承自db.Model的类，代表数据库中的一张表
class Article(db.Model):
    #定义一个整数类型的主键列id
    id = db.Column(db.Integer, primary_key=True)
    #定义一个字符串类型的列title,最大长度为200，且不能为空
    title = db.Column(db.String(200), nullable=False)
    #定义一个文本类型的列content,用于存储文章内容，不能为空
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


##################创建一个表单类ArticleForm###################
#创建一个继承自FlaskForm的表单类
class ArticleForm(FlaskForm):
    #定义一个字符串输入字段title，标签为Title，并使用DataRequired验证器确保该字段不为空
    title = StringField('Title', validators=[DataRequired(), Length(1, 200)])
    #定义一个文本区域输入字段content，标签为Content，同样使用DataRequired验证器
    content = TextAreaField('Content', validators=[DataRequired()])
    #定义一个提交按钮，标签为submit
    submit = SubmitField('Submit')

###################定义/write路由，处理文章的书写和提交##################

#定义/write路由，支持GET和POST请求
@app.route('/write',methods=['GET','POST'])
def publish():
    #创建一个ArticleForm实例
    form = ArticleForm()
    #检查表单是否通过验证并提交
    if form.validate_on_submit():
        #获取表单中输入和内容
        title = form.title.data
        content = form.content.data
        # 创建一个新的Article对象
        article = Article(title=title, content=content)
        #将新的文章对象添加到数据库会话中
        db.session.add(article)
        #提交数据库会话，将数据保存到数据库
        db.session.commit()
        #显示提示消息
        flash('Article published successfully!')
        #重定向到文章列表页面
        return redirect(url_for('article_list'))
    #如果是get请求或表单验证失败，渲染write_article.html模板并传递表单实例
    return render_template('write_article.html',form=form)




###################定义/articles路由，显示文章列表###############
#定义一个路由，处理/articles的请求
@app.route("/articles")
def article_list():
    #从数据库中查询所有文章记录
    articles = Article.query.all()
    #渲染article_list.html模板并传递文章列表
    return render_template("article_list.html", articles=articles)

###################在启动时创建数据库，并以调试模式运行应用##################

if __name__ == '__main__':
    #创建应用上席文，确保可以在应用外部使用数据库操作
    with app.app_context():
        #创建所有定义的数据库表单
        db.create_all()
    #以调试模式运行Flask应用
    app.run(debug=True)
