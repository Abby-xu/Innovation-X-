var setTheme = localStorage.getItem('theme');
console.log('theme',setTheme);

if (setTheme == null) {
    swapStyles("static/css/app.css");
}
else {
    swapStyles(setTheme);
}


function swapStyles(sheet) {
    document.getElementById('mystylesheet').href = sheet;
    localStorage.setItem('theme',sheet);
}