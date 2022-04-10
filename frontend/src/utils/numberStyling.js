
const getOrder = (number) => {
    if (number % 100 >= 11 && number % 100 <= 13) {
        return 'th'
    }
    if (number % 10 === 1) {
        return 'st'
    }
    if (number % 10 === 2) {
        return 'nd'
    }
    if (number % 10 === 3) {
        return 'rd'
    }
    return 'th'
}

export {getOrder};
