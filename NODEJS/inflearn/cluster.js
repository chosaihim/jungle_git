var cluster = require("cluster");

//Round Robin 방식으로 cluster
cluster.schedulingPolicy = cluster.SCHED_RR;

if(cluster.isMaster == true) {
    console.log("시작")
    cluster.fork();
    cluster.fork();
    cluster.fork();

    cluster.on('online',function(worker){
        for(var i =0 ;i <10; i++){
            console.log(worker.process.pid, "동작");
        }
        console.log("end function");
    })

    console.log("끝");
}
