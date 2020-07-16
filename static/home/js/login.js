let formError = {
    email: '',
    password: '',
};

// Dynamic Form Validation
$('#login-form').on('change past keyup', ':input',  (e) => {
    // Defaults
    const name = e.target.name;
    const value = e.target.value;
    const fieldError = {};
    const { error } = validate({[name]: value}, fieldError);
    formError = {...formError, [name]: error[name]}
    dispatchErrors(formError)
});

// Handle Submitting
$('input[type="submit"]', '#login-form').on('click', (e) => {
    e.preventDefault();
    const { isValid, error} = validate(objectifyForm($('#login-form').serializeArray()), formError);
    dispatchErrors(error);
    if(isValid) {
        $('#login-form').submit();
    }

})



// Validate Form Data
const validate = (data, error) => {
    // Default Regex
    const email_re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;


    if (data.email && !email_re.test(data.email.toLowerCase())) error.email = 'Invalid Email'
    else error.email = ''

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



