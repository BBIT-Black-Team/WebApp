let formError = {
    email: '',
    password1: '',
    password2: '',
    first_name: '',
    last_name: '',
};

// Dynamic Form Validation
$('#register-form').on('change past keyup', ':input',  (e) => {
    // Defaults
    const name = e.target.name;
    const value = e.target.value;
    const fieldError = {};
    const { error } = validate({[name]: value}, fieldError);
    formError = {...formError, [name]: error[name]}
    dispatchErrors(formError)
});

// Handle Submitting
$('input[type="submit"]', '#register-form').on('click', (e) => {
    e.preventDefault();
    const { isValid, error} = validate(objectifyForm($('#register-form').serializeArray()), formError);
    dispatchErrors(error);
    if(isValid) {
        $('#register-form').submit();
    }

})



// Validate Form Data
const validate = (data, error) => {
    const password1 = $('#id_password1').val();
    const email = $('#id_email').val();

    // Default Regex
    const email_re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;


    if (data.email && !email_re.test(data.email.toLowerCase())) error.email = 'Invalid Email'
    else error.email = ''

    if (data.password1) {
        if (data.password1.length < 8) error.password1 = 'Your password must contain at least 8 characters.'
        else if (/^\d+$/.test(data.password1)) error.password1 = 'Your password can’t be entirely numeric.'
        else if (email && email === data.password1) error.password1 = 'Your password can’t be too similar to your other personal information.'
        else error.password1 = '';
    }

    if(data.password2 && password1 !== data.password2) error.password2 = "Password doesn't match.";
    else error.password2 = '';

    for(const field of Object.keys(data)){
        if (!data[field]) error[field] = 'This field is required.'
    }

    const isValid = () => {
        for(const field of Object.keys(error))
            if(error[field]) return false;
            return true;
    };

    return({ isValid: isValid() , error})

}


// Shows Error
const dispatchErrors = (error) => {
    for(const field of Object.keys(error)) {
        const elem = document.getElementById(`id_${field}`)
        if(elem) {
            if (error[field]) {
                $(elem).addClass('error-div');
                document.getElementById(`error_${field}`).innerHTML = error[field];
            }
                else {
                    $(elem).removeClass('error-div');
                    document.getElementById(`error_${field}`).innerHTML = '';
                }
        }
    }

}

// Objectify Form
function objectifyForm(formArray) {//serialize data function

  const returnArray = {};
  for (let i = 0; i < formArray.length; i++){
    returnArray[formArray[i]['name']] = formArray[i]['value'];
  }
  return returnArray;
}
