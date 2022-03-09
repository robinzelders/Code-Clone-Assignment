function calculateFactorial(input){

    if (input<=2){
        return input;
    }

    let result=input;
    let offset=1;

    while(offset<input){
        result=result*(input-offset);
    }

    return result;
}