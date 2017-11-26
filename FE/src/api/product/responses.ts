
export interface ApiResProductDetail{
    id: number;
    name: string;
    describe: string;
    price: number;
    first_pay_price: number;
    cover: string;
}

export interface ApiResProducts{
    results: ApiResProductDetail[];
    pages: number;
}


