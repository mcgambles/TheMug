const mainContainer = document.getElementById('containerShow');

function showForms(){
    const indexForms = document.getElementById('LogAndReg');
    if(indexForms.className !== "LogAndReg"){
        indexForms.className = "LogAndReg";
    }
    else{
        indexForms.className = 'LogAndRegAnimate';
    }
}




