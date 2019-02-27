
// f : (t,[x,y,...]) -> int

// шаг метода Рунге-Кутта
runge_step = (t, start, functions, step_size) => {
    let range = functions.length;
    let k1 = [];
    let k2 = [];
    let k3 = [];
    let k4 = [];
    for (let i = 0 ; i < range ; i++ ){
        k1.push(functions[i](t,start)*step_size)
    }
    for (let i = 0 ; i < range ; i++ ){
        k2.push(functions[i](t + step_size/2,start.map((value,j) =>{
            return k1[j]/2 + value
        }))*step_size)
    }
    for (let i = 0 ; i < range ; i++ ){
        k3.push(functions[i](t + step_size/2,start.map((value,j) =>{
            return k2[j]/2 + value
        }))*step_size)
    }
    for (let i = 0 ; i < range ; i++ ){
        k4.push(functions[i](t + step_size,start.map((value,j) =>{
            return k3[j] + value
        }))*step_size)
    }
    return k1.map((value,i)=>{
        return start[i] + (k1[i] + 2 * (k2[i]+k3[i]) + k4[i])/6
    })
};

runge_kutt = (props) => {
    const {start_time , end_time , steps} = props;
    const step = (end_time - start_time) / steps;
    let {functions, start} = props;

    let time = [];
    for (let t = start_time; t <= end_time; t += step) {
        time.push(t)
    }

    let result = [start];
    for (let i = 0; i < steps; i++) {
        let next = this.runge_step(time[i], result[result.length - 1], functions, step);
        result.push(next)
    }

    return [result,time];
};