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
    console.log(runge_kutt(config))
};

main();