const deepMerge = (defaultObj: object, overridesObj: object) =>
    Object.fromEntries(
        Object.entries(defaultObj).map(([key, value]) => [
            key,
            value instanceof Object && overridesObj[key] instanceof Object ? deepMerge(value, overridesObj[key]) : (overridesObj[key] ?? value),
        ])
    );

export default deepMerge;
