let main;

let listener = (id) =>{
    let slider = document.getElementById(id+"range");
    let output = document.getElementById(id+"output");
    output.innerHTML = slider.value;
    slider.oninput = function() {
        output.innerHTML = this.value;
        main()
    };
};

listener("R");
listener("B");
listener("V");
listener("P");
listener("A");


//система дифф уравнений
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


// метод Рунге-Кутта
my_runge_kutt = (props) => {
    const {start_time , step , steps} = props;
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
    if( time.length < steps){
        props.step = props.step / (steps / time.length + 1);
        return my_runge_kutt(props)
    }
    return [result,time];
};

main = () => {
    // инициализация
    const g = 9.8;
    const r = document.getElementById("Rrange").value;
    const p = document.getElementById("Prange").value;
    const m = p * 4/3 * Math.PI * Math.pow(r,3);
    const C = 0.15;
    const ro = 1.29;
    const S = 2 * Math.PI * r;
    const props = {
        m:m,
        g:g,
        b:0
    };
    const v = document.getElementById("Vrange").value;
    const ang = Math.PI * document.getElementById("Arange").value/180;
    const funcs = functions(props);
    const config = {
        start_time : 0 ,
        end_time : 10 ,
        steps : 1000,
        step : 1/100,
        functions : funcs,
        start : [0,0,v*Math.cos(ang),v*Math.sin(ang)]
    };

    // запуск модели ньютона
    let [res , time] = my_runge_kutt(config);

    // интерполяция для последних 2-х точек
    let [last,prev_last] = [res[res.length -1], res[res.length -2]];
    let [y1,y0,x1,x0]  = [last[1],prev_last[1],last[0],prev_last[0]];
    let k = (y1-y0)/(x1-x0);
    let b = y0 -k*x0;
    let last_x = -b/k;

    res[res.length -1][0] = last_x;
    res[res.length -1][1] = 0;


    // модель Галилея
    let [gal_x,gal_y] = [[0],[0]];
    let x_drop = Math.tan(ang)*2*v*v*Math.cos(ang)*Math.cos(ang)/props.g;
    let t_drop = x_drop/(v*Math.cos(ang));
    let steps = 100;
    let step_size = t_drop/steps;
    let t = [0];
    let x_func = (t) => v * Math.cos(ang) * t;
    let y_func = (t) => v * Math.sin(ang) * t - g * t * t/2;
    while (steps > 0){
        t.push(t[t.length-1]+step_size);
        gal_x.push(x_func(t[t.length-1]));
        gal_y.push(y_func(t[t.length-1]));
        steps--;
    }

    console.log(gal_x[gal_x.length-1], last_x, Math.abs(last_x-gal_x[gal_x.length-1]));
    // создание графиков
    let plot = document.getElementById('plot');
    Plotly.newPlot( plot, [
        {
        x: res.map(el => el[0]),
        y: res.map(el => el[1]),
            mode: 'lines',
            name: 'Newton'
        },
        {
            x:gal_x,
            y:gal_y,
            mode: 'lines',
            name: 'Gal'
        }
    ], {
        margin: { t: 0 } } );
};

main();