/* ---------------------------------------------------
    Statistical utilities
*/
function boxMuller() {
    var w = 10000.,
        x1, x2;

    while (w >= 1.) {
        x1 = 2.0*Math.random() - 1.0;
        x2 = 2.0*Math.random() - 1.0;
        w = x1*x1 + x2*x2;
    }

    w = Math.sqrt(-2.0*Math.log(w) / w);
    // y1 = x1 * w;
    // y2 = x2 * w;
    return x1*w;
}

function gaussian(mean, std) {
    /*
        Sample from a Gaussian distribution with specified
        mean and standard deviation.
    */
    if (mean === undefined || std === undefined) {
        throw "Gaussian needs 2 arguments (mean, standard deviation)";
    }
    return boxMuller()*std + mean;
}

/* ---------------------------------------------------
    Integration
*/
function LeapfrogIntegrator(potential) {
    /*
        Leapfrog integration. Extra arguments passed to this initializer
        will get passed to the potential.acceleration_at() method.
    */
    this.potential = potential;
    this.func_args = arguments;

    this.step = function(t, ws, dt) {
        /*
            Step forward the vector w by the given timestep
        */

        var new_ws = new Array();
        for (var j=0; j < ws.length; j++) {
            var w = ws[j],
                halfLen = parseInt(w.length/2);

            var q = w.slice(0,halfLen),
                p = w.slice(halfLen),
                new_q = new Array(),
                new_p = new Array();

            var ai = this.potential.acceleration_at(q, t, arguments);
            for (var i=0; i < q.length; i++) {
                new_q[i] = q[i] + p[i]*dt + 0.5*ai[i]*dt*dt;
            }

            var new_ai = potential.acceleration_at(new_q, t+dt, arguments);
            for (var i=0; i < p.length; i++) {
                new_p[i] = p[i] + 0.5*(ai[i] + new_ai[i])*dt;
            }

            new_ws.push(new_q.concat(new_p));
        }
        return new_ws;
    }

    this.run = function(w0s, dt, nsteps, t1) {
        /*
            Run the integrator from initial conditions w0s with
            timestep dt for nsteps.
        */
        if (t1 == undefined) {
            t1 = 0.
        }

        var nparticles = w0s.length,
            ndim = w0s[0].length,
            times = new Array(),
            ws = new Array();

        // add initial positions/velocities to the array
        ws.push(w0s);
        t = t1;
        for (var n=1; n <= nsteps; n++) {
            ws[n] = this.step(t, ws[n-1], dt);
            times.push(t);
            t += dt;
        }

        return {
            "time" : times,
            "ws" : ws
        };
    }
}

/* ---------------------------------------------------
    Potentials
*/
function KeplerPotential(r0, k) {
    this.k = k;
    this.r0 = r0;

    this._r_to_R = function(r) {
        var tmp,
            R = 0;
        for (var i=0; i < r.length; i++) {
            tmp = r[i] - this.r0[i];
            R += tmp*tmp;
        }
        return Math.sqrt(R);
    }

    this.value_at = function(r) {
        return -this.k/this._r_to_R(r);
    }

    this.acceleration_at = function(r) {
        var R = this._r_to_R(r),
            acc = new Array();

        for (var i=0; i < r.length; i++) {
            acc.push(-this.k * r[i] / (R*R*R));
        }
        return acc;
    }
}

function AxisymLogPotential(r0, vc, q, rc) {
    this.vc = vc;
    this.q = q;
    this.rc = rc;
    this.r0 = r0;

    this._shift_r = function(r) {
        var shift_r = new Array();
        for (var i=0; i < r.length; i++) {
            shift_r.push(r[i] - this.r0[i]);
        }
        return shift_r;
    }

    this.value_at = function(r) {
        r = this._shift_r(r);
        var x = r[0],
            y = r[1];
        return this.vc*this.vc*Math.log(x*x + y*y/(this.q*this.q) + this.rc*this.rc);
    }

    this.acceleration_at = function(r) {
        r = this._shift_r(r);
        var x = r[0],
            y = r[1];

        fac = -this.vc*this.vc / (x*x + y*y/(this.q*this.q) + this.rc*this.rc);
        return [fac*x, fac*y/(this.q*this.q)];
    }
}

function HenonHeilesPotential(r0) {
    this.r0 = r0;

    this._shift_r = function(r) {
        var shift_r = new Array();
        for (var i=0; i < r.length; i++) {
            shift_r.push(r[i] - this.r0[i]);
        }
        return shift_r;
    }

    this.value_at = function(r) {
        r = this._shift_r(r);
        var x = r[0],
            y = r[1];
        return 0.5*(x*x + y*y + 2*x*x*y - 2./3.*y*y*y)
    }

    this.acceleration_at = function(r) {
        r = this._shift_r(r);
        var x = r[0],
            y = r[1];

        return [-2*x*y - x, -x*x + y*y - y];
    }
}

/* ---------------------------------------------------
    Drawing
*/
function PointStyle(color, alpha, size) {
    this.color = color;
    this.alpha = alpha;
    this.size = size;
}