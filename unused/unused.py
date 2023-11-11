


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///filmflix.db'
bcrypt = Bcrypt(app)

conn = sql.connect('filmflix.db')

class User():
    conn = get_db_connection()
    id = conn.Column(conn.Integer, primary_key=True)
    username = conn.Column(conn.String(20), unique=True, nullable=False)
    password = conn.Column(conn.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}')"
    






class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('index'))
       


    return render_template('register.html', title='Register', form=form)



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'admin' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful', 'danger')
    
    return render_template('login.html', title='Login', form=form)










@app.route('/delete_user/<int:userID>', methods=['POST'])
def delete_user(userID):
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (userID,))
    conn.commit()
    conn.close()
    flash('User deleted successfully.')
    return redirect(url_for('admin_dashboard'))  



