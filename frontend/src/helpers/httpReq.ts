import filePath from "@/helpers/filePath.ts";

const apiPath = filePath.httpClient()

console.log("http: " + apiPath);

function myFetch({ url, method = "GET", headers, body }) {
    return fetch(url, {
        method, // *GET, POST, PUT, DELETE, etc.
        // mode: "cors", // *cors, no-cors, same-origin
        // cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        // credentials: "same-origin", // *same-origin, include, omit
        // redirect: "follow", // *follow, manual, error
        // referrerPolicy: "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        headers,
        // headers: {
        //     "Content-Type": "application/json",
        //     "Content-Type": "application/x-www-form-urlencoded",
        // },
        body,
    });
}

const httpReq = {
    get: {
        // http://localhost:3000/api/endpoint
        json: (endpoint) => {
            const reqData = {
                url: apiPath + endpoint,
                method: "GET",
            };

            return myFetch(reqData)
                .then((res) => {
                    if (res.ok) {
                        return res.json(); // если HTTP-статус в диапазоне 200-299
                    } else {
                        return Promise.reject({
                            msg: "httpReq [ERR] get.json",
                            res,
                        });
                    }
                })
                .catch((err) => {
                    if (err.stack) err.stack = err.stack.split("\n");

                    const errObj = {
                        msg: err.msg ? err.msg : "httpReq [ERR] get.json",
                        reqData,
                        res: err.res,
                        err,
                    };

                    console.error(errObj);
                    return Promise.reject(errObj);
                });
        },
    },
    post: {
        // http://localhost:3000/api/endpoint
        json: (endpoint, payload = {}) => {
            const reqData = {
                url: apiPath + endpoint,
                method: "POST",

                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
            };

            return myFetch(reqData)
                .then((res) => {
                    if (res.ok) {
                        return res.json(); // если HTTP-статус в диапазоне 200-299
                    } else {
                        return Promise.reject({
                            msg: "httpReq [ERR] post.json",
                            res,
                        });
                    }
                })
                .catch((err) => {
                    if (err.stack) err.stack = err.stack.split("\n");

                    const errObj = {
                        msg: err.msg ? err.msg : "httpReq [ERR] post.json",
                        payload,
                        reqData,
                        res: err.res,
                        err,
                    };

                    console.error(errObj);
                    return Promise.reject(errObj);
                });
        },
    },
};

export default httpReq;
