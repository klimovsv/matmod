functions = (props) =>{
    let {m, g, b} = props;
    return [
        //x
        (t,args) => {
            let [x,y,u,w] = args;
            return u;
        },
        //y
        (t,args) => {
            let [x,y,u,w] = args;
            return w;
        },
        //u
        (t,args) => {
            let [x,y,u,w] = args;
            return (-b * u * Math.sqrt(u*u + w*w))/m
        },
        //w
        (t,args) => {
            let [x,y,u,w] = args;
            return ( -m*g - b * w * Math.sqrt(u*u + w*w))/m
        }
    ];
};


my_runge_kutt = (props) => {
    const {start_time , end_time , steps} = props;
    const step = (end_time - start_time) / steps;
    let {functions, start} = props;

    let time = [start_time];
    let result = [start];
    let i = 0;
    while (result[i][1] >= 0 ){
        let next = this.runge_step(time[i], result[result.length - 1], functions, step);
        result.push(next);
        time.push(time[time.length-1]+step);
        i++;
    }
    return [result,time];
};

main = () => {
    let props = {
        m:100,
        g:9.8,
        b:0
    };
    const v = 10;
    const ang = Math.PI/4;
    const funcs = functions(props);
    const config = {
        start_time:0 ,
        end_time: 10 ,
        steps : 100,
        functions : funcs,
        start : [0,0,v*Math.cos(ang),v*Math.sin(ang)]
    };
    let [res , time] = my_runge_kutt(config);

    let [last,prev_last] = [res[res.length -1], res[res.length -2]];
    let [y1,y0,x1,x0]  = [last[1],prev_last[1],last[0],prev_last[0]];
    let k = (y1-y0)/(x1-x0);
    let b = y0 -k*x0;
    let last_x = -b/k;

    res[res.length -1][0] = last_x;
    res[res.length -1][1] = 0;

    let [gal_x,gal_y] = [[],[]];
    let x_drop = Math.tan(ang)*2*v*v*Math.cos(ang)*Math.cos(ang)/props.g;
    let t_drop = x_drop/(v*Math.cos(ang));
    let steps = 20;
    let step_size = t_drop/steps;
    let t = [0];


    let plot = document.getElementById('plot');
    Plotly.plot( plot, [{
        x: res.map(el => el[0]),
        y: res.map(el => el[1]) }], {
        margin: { t: 0 } } );
};

main();