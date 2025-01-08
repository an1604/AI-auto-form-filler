
export const fillFieldByClass = (classname, value) => {
    const element = document.querySelector(classname);
    try {
        element.value = value;
        element.dispatchEvent(new Event('input'));
        return true;
    } catch (e) {
        alert(e);
        return false;
    }
}

module.exports(sendRequest)