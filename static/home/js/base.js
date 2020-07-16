// Objectify Form
function objectifyForm(formArray) {//serialize data function

  const returnArray = {};
  for (let i = 0; i < formArray.length; i++){
    returnArray[formArray[i]['name']] = formArray[i]['value'];
  }
  return returnArray;
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
