exports.getCurrentDateString = function getCurrentDateString(currentDate = new Date()){
    return `${currentDate.getFullYear()}-${currentDate.getMonth() + 1}-${currentDate.getDate()}`
}
