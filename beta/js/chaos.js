/*
    Code for visualizing chaotic and regular orbits in the
    Henon-Heiles potential.
*/
var chaosSimulation;
function ChaosSimulation(context, potential, pixelScale, dt) {
    this.context = context;
    this.potential = potential;
    this.pixelScale = pixelScale;
    this.dt = dt;
    this.orbits = {};

    // define an integrator
    this.integrator = new LeapfrogIntegrator(this.potential);

    this.update = function() {
        for (var key in this.orbits) {
            this.orbits[key].w = this.integrator.step(0., [this.orbits[key].w], this.dt)[0];
        }
    }

    this.draw = function(wipe) {
        if (wipe == undefined)
            wipe = false;

        if (wipe == true)
            this.context.clearRect(0, 0, this.context.canvas.width, this.context.canvas.height);

        var w, ps, preAlpha;
        for (var key in this.orbits) {
            w = this.orbits[key].w;
            ps = this.orbits[key].pointStyle;

            preAlpha = this.context.globalAlpha;
            this.context.globalAlpha = ps.alpha;
            this.context.beginPath();
            this.context.fillStyle = ps.color;
            this.context.arc(w[0]*this.pixelScale, w[1]*this.pixelScale,
                             ps.size, 0, Math.PI*2,true);
            this.context.closePath();
            this.context.fill();
            this.context.globalAlpha = preAlpha;
        }
    }
}

// Can't go inside simulation object
function chaosDrawUpdate() {
    canvas = chaosSimulation.context.canvas;
    //chaosSimulation.context.clearRect(0, 0, canvas.width, canvas.height);
    chaosSimulation.draw();
    chaosSimulation.update();
}

function make_chaos(canvas) {
    // Display parameters
    var pixScale = 250,
        alpha = 0.2,
        dt = 0.1,
        context = canvas.getContext('2d'),
        interval;

    // has to go after context definition!?!
    canvas.width = $(".canvas-container").width();
    canvas.height = $(".canvas-container").height();

    // put the origin at the center of the canvas
    var x0 = canvas.width / 2. / pixScale,
        y0 = canvas.height / 2. / pixScale;

    // define the potential and simulation
    var potential = new HenonHeilesPotential([x0, y0]);
    chaosSimulation = new ChaosSimulation(context, potential, pixScale, dt);

    // Cycle through resonant orbits in R,z?
    var regular1 = {
        w : [x0+0., y0+0.3, 0.421900462195, 0.],
        pointStyle : new PointStyle("#eeeeee", 0.25, 2.)
    };
    var regular2 = {
        w : [x0+0., y0+0., 0.433012701892, 0.25],
        pointStyle : new PointStyle("#f4a582", 0.25, 2.)
    };

    var chaotic1 = {
        w : [x0+0., y0-0.2, 0.452401002062, 0.],
        pointStyle : new PointStyle("#92c5de", 0.25, 2.)
    };
    var chaotic2 = {
        w : [x0+0., y0+0.2, 0.418728233265, 0.2],
        pointStyle : new PointStyle("#a6d96a", 0.25, 2.)
    };

    chaosSimulation.orbits['regular1'] = regular1;
    $("#regular").addClass("underline");
    //chaosSimulation.orbits['regular2'] = regular2;
    //chaosSimulation.orbits['chaotic1'] = chaotic1;
    //chaosSimulation.orbits['chaotic2'] = chaotic2;

    chaosSimulation.draw();

    $("#startChaos").click(function() {
        interval = setInterval(chaosDrawUpdate, 5);
    });
    $("#stopChaos").click(function() {
        clearInterval(interval);
    });

    $("#regular").click(function() {
        if ($(this).hasClass("underline")) {
            delete chaosSimulation.orbits["regular1"];
            $(this).removeClass("underline");
            chaosSimulation.draw(true);
        } else {
            chaosSimulation.orbits["regular1"] = regular1;
            $(this).addClass("underline");
        }
    });

    $("#chaotic").click(function() {
        if ($(this).hasClass("underline")) {
            delete chaosSimulation.orbits["chaotic1"];
            $(this).removeClass("underline");
            chaosSimulation.draw(true);
        } else {
            chaosSimulation.orbits["chaotic1"] = chaotic1;
            $(this).addClass("underline");
        }
    });

    // draw the zero velocity curve
    var ngrid = 1000,
        miny = -0.5,
        maxy = 2.,
        E = 1./8.;
    var dy = (maxy - miny) / parseFloat(ngrid);

    var pts = new Array();
    y = miny;
    for (var i=0; i<ngrid; i++) {
        x = Math.sqrt(((2/3.)*y*y*y - y*y + 2*E) / (2*y + 1));

        context.beginPath();
        context.fillStyle = "rgba(202, 0, 32, 0.2)";
        context.arc(x0*pixScale - x*pixScale, (y+y0)*pixScale, 1, 0,
                         Math.PI*2,true);
        context.closePath();
        context.fill();

        context.beginPath();
        context.fillStyle = "rgba(202, 0, 32, 0.2)";
        context.arc(x0*pixScale+x*pixScale, (y+y0)*pixScale, 1, 0,
                         Math.PI*2,true);
        context.closePath();
        context.fill();
        y += dy
    }
    // chaosContext.restore()
}