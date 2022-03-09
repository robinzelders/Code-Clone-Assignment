function calculateFactorial(x){

    if (x <= 2) {
        return x;
    }

    let result = x;
    let offset = 1;

    while(offset < x){
        result = result * (x - offset);
    }

    return result;
}