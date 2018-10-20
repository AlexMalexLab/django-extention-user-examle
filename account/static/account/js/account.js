//Account
window.addEventListener('load', function () {
    //Login
    var form = document.querySelector('.form_login');
    if (form) {
        var mixin = {
            el: form,
            data() {
                return {
                    values: { login: '', password: '' },
                    dst: { url: '/account/api/login/' },
                }
            },
            methods: {acceptResponse:  function (data) { location.href = '/account/profile/'; }}
        }
        var vm = _form.initVueForm(mixin);
    }

    //Restore Access
    var form = document.querySelector('.form_restore-access');
    if (form) {
        var mixin = {
            el: form,
            data() {
                return {
                    values: {login: ''},
                    dst: { url: '/account/api/restore_access/' }
                }
            },
        }
        var vm = _form.initVueForm(mixin);
    }

    //Registration
    var form = document.querySelector('.form_reg');
    if (form) {
        var mixin = {
            el: form,
            data() {
                return {
                    values: { login: '', name:'', password:'', 'password_confirm': '', notify: false },
                    dst: { url: '/account/api/' },
                    multipart: true,
                    change_files: []
                }
            },
            methods: {
                acceptResponse:  function (data) { location.href = '/account/profile/'; },
                validate: function () {
                    if (!this.values['notify']) {
                        this.errors['notify'].push(_gl.itemDict.acceptRules);
                        return false;
                    }
                    if (this.values['password'] != this.values['password_confirm']) {
                        this.errors['password'].push(_gl.itemDict.confirmPassword);
                        return false;
                    }
                    return true;
                },
                selectImg: function () {
                    this.$el.querySelector(".imgf").click();
                }
            }
        }
        var vm = _form.initVueForm(mixin);
    }


    //Profile
    var form = document.querySelector('.form-profile');
    if (form) {
        var endPoint = "/account/api/"+form.getAttribute('data-id')+"/";
        var mixin = {
            el: form,
            data() {
                return {
                    values: {
                        login: '', name:'', password: '', 'password_confirm': '',
                        birthday: '', country: '', city: '', interests: '', 'ya_purse': '',

                    },
                    skipEmptyFields: ['password', 'password_confirm', 'avatar'],
                    dst: { url: endPoint, method: "PATCH" },
                    src: { url: endPoint },
                    multipart: true,
                    files: { avatar: '' }
                }
            },
            methods: {
                acceptResponse:  function (data) { location.href = '/account/profile/'; },
                validate: function () {
                    if (this.values['password'] != this.values['password_confirm']) {
                        this.errors['password'].push(_gl.itemDict.confirmPassword);
                        return false;
                    }
                    return true;
                },
                selectImg: function () {
                    this.$el.querySelector(".imgf").click();
                }
            }
        }
        var vm = _form.initVueForm(mixin);
    }


    //Logout
    var logouts = document.getElementsByClassName("logout");
    if (logouts.length) {
        function logout() {
            axios({
                method: 'POST', url: '/account/api/logout/',
                headers: { 'X-CSRFToken': _gl.getCSRFToken() }
            }).then(function (response) {
               location.reload();
            });
        }
        for(var i = 0; i < logouts.length; i++) {
            logouts[i].addEventListener('click', logout);
        }
    }



});
