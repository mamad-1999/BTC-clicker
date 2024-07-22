function formatNumber(number) {
    const units = [
        { value: 1e9, symbol: 'B' },
        { value: 1e6, symbol: 'M' },
        { value: 1e3, symbol: 'K' }
    ];

    for (let unit of units) {
        if (Math.abs(number) >= unit.value) {
            let formattedValue = number / unit.value;
            if (Number.isInteger(formattedValue)) {
                return `${formattedValue}${unit.symbol}`;
            } else {
                return `${formattedValue.toFixed(2).replace(/\.?0+$/, '')}${unit.symbol}`;
            }
        }
    }

    return number.toString();
}

export default formatNumber