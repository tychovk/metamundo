"use strict";

var init_canvas = function(world_object, blobs) {

    var canvas, context, viewportSize;

    // viewport

    var VP = { X: 0, 
               Y: 0, 
               WIDTH: 20 * 35 ,    // keep this one divisable by the speed for now. Default: 512
               HEIGHT: 20 * 15 };  // keep this one divisable by by the speed for now. Default: 352

    var player_colliding = false;

    const FIELD_SIDE_SIZE = 32;

    const NUM_OF_TILES = 2;

    const NUM_OF_BLOBS = 1;

    const BLOB_SIZE = 9;

    const PLAYER_SIZE = 16;

    const world = world_object[0].fields;

    let playerInfo = { x: 0,
                       y: 0 };

    var Game = function(canvasId) {
        function loadMap(map) {
            let width_x = world.x_upper_bound - world.x_lower_bound;
            let height_y = world.y_upper_bound - world.y_lower_bound;


            let world_map = [];
            let top_line = [];
            let border_line = [];

            for (let x = 0; x <= width_x + 2; x++) {
                border_line.push(0);
            }
            world_map.push(border_line);


            for (let y = 0; y <= height_y; y++) {
                let y_line = [];
                y_line.push(0); // add border on the right side

                for (let x = 0; x <= width_x; x++) {
                    y_line.push(1);
                }
                
                y_line.push(0); // add border on the left side
                world_map.push(y_line);
            }
            
            world_map.push(border_line);
            // console.log('worldmap', world_map);
            return world_map;
        };



        canvas = document.getElementById(canvasId);
        context = canvas.getContext('2d');
        let worldGrid = loadMap(1);
        let worldSize = { x: worldGrid[0].length - 1,
                          y: worldGrid.length - 1,
                          width: (worldGrid[0].length) * FIELD_SIDE_SIZE,
                          height: (worldGrid.length) * FIELD_SIDE_SIZE
                        };
        

        canvas.width = VP.WIDTH;// window.innerWidth; //512;
        canvas.height = VP.HEIGHT; //window.innerHeight; //352;
        // console.log(VP.WIDTH);
        // console.log(worldSize.width);
        if (VP.WIDTH > worldSize.width) {
            canvas.width = worldSize.width;
            VP.WIDTH = worldSize.width;
        }
        if (VP.HEIGHT > worldSize.height) {
            canvas.height = worldSize.height;
            VP.HEIGHT = worldSize.height;
        }


        let tiles = this.tileImages(NUM_OF_TILES);
        let blob_images = this.blobImages(NUM_OF_BLOBS);

        let player = new Player(this, VP, playerInfo, Keyboarder);
        this.draw(context, VP, worldGrid, worldSize, tiles, blob_images, blobs, player);

        canvas.addEventListener('keydown', function(e) {
            console.log(e);
        });

        canvas.tabIndex = 0;
        canvas.focus();
        canvas.addEventListener('keydown', function(e) {
            console.log(e);
            var key = e.keyCode;
            if (key == 37) {
                // Left
                if (player.x > 0) player.x -= 16;
            }

            if (key == 38) {
                // Up
                if (player.y > 0) player.y -= 16;
            }

            if (key == 39) {
                // Right
                if (player.x < (worldSize.width - player.size.x)) player.x += 16;
            }

            if (key == 40) {
                // Down
                if (player.y < (worldSize.height - player.size.y)) player.y += 16;
            }
            // Okay! The player is done moving, now we have to determine the "best" viewport.
            // Ideally the viewport centers the player,
            // but if its too close to an edge we'll have to deal with that edge

            VP.X = player.x - Math.floor(0.5 * VP.WIDTH);
            if (VP.X < 0) VP.X = 0;
            if (VP.X + VP.WIDTH > worldSize.width) VP.X = worldSize.width - VP.WIDTH;          
            
            VP.Y = player.y - Math.floor(0.5 * VP.HEIGHT);
            if (VP.Y < 0) VP.Y = 0;
            if (VP.Y + VP.HEIGHT > worldSize.height) VP.Y = worldSize.height - VP.HEIGHT;
            //console.log("VP y" + VP.Y);
            //Game.draw(context, VP, worldGrid, worldSize, tiles, blob_images, blobs, player);

            //let y_grid = Math.floor(VP.Y / FIELD_SIDE_SIZE);
            //let x_grid = Math.floor(VP.X / FIELD_SIDE_SIZE);

            //console.log(y_grid);
            //console.log(x_grid);
            //console.log(player.y);
            //console.log(worldSize.height);
            //console.log(worldSize.y);
            //console.log(player.x);
            //console.log(worldSize.width);
            //console.log(worldSize.x);

        }, false);

        if (canvas.addEventListener) console.log("event listener is here");
    

        var tick = function(context, VP, worldGrid, worldSize, NUM_OF_TILES, player) {
            //let tiles = this.tileImages(NUM_OF_TILES);
            //let blob_images = this.blobImages(NUM_OF_BLOBS);
            //console.log("vp" + VP);
            //console.log("worldGrid" + worldGrid);

            this.draw(context, VP, worldGrid, worldSize, tiles, blob_images, blobs, player);
            requestAnimationFrame(tick);
        }.bind(this, context, VP, worldGrid, worldSize, NUM_OF_TILES, player);
        tick();
     
    };


    Game.prototype = {

        tileImages: function(NUM_OF_TILES) {
            let tiles = [];
            for (let i = 0; i <= NUM_OF_TILES; i++) {
                let imageObj = new Image();
                imageObj.src = "/static/imgs/t" + i + ".png";
                tiles.push(imageObj);
            };
            return tiles;
        },

        blobImages: function(NUM_OF_BLOBS) {
            let blob_images = [];
            for (let i = 1; i <= NUM_OF_BLOBS; i++) {
                let imageObj = new Image();
                imageObj.src = "/static/imgs/b" + i + ".png";
                blob_images.push(imageObj);
            };
            return blob_images;
        },

        addBody: function(body) {
            this.bodies.push(body);
        },

        draw: function(context, VP, worldGrid, worldSize, tiles, blob_images, blobs, player) {
            context.clearRect(0, 0, VP.WIDTH, VP.HEIGHT);
            let x_max, y_max;

            let height_fields = VP.HEIGHT / FIELD_SIDE_SIZE;
            let width_fields = VP.WIDTH / FIELD_SIDE_SIZE;

            y_max = Math.ceil(height_fields) - 1;
            x_max = Math.ceil(width_fields) - 1;

            // checks which fields should be (pre) prendered.
            if (VP.X % FIELD_SIDE_SIZE != 0) {
                if (VP.X + VP.WIDTH <= worldSize.width - FIELD_SIDE_SIZE || VP.WIDTH % FIELD_SIDE_SIZE == 0) {
                    x_max = Math.ceil(width_fields);
                }
            }

            if (VP.X + VP.WIDTH > worldSize.width - FIELD_SIDE_SIZE) {
                if ((VP.WIDTH - (VP.X + VP.WIDTH - (worldSize.width - FIELD_SIDE_SIZE))) / FIELD_SIDE_SIZE > Math.floor(width_fields)) {
                    x_max = Math.ceil(width_fields);
                }
            }

            if (VP.Y % FIELD_SIDE_SIZE != 0) {
                if (VP.Y + VP.HEIGHT <= worldSize.height - FIELD_SIDE_SIZE || VP.HEIGHT % FIELD_SIDE_SIZE == 0) {
                    y_max = Math.ceil(height_fields);
                }
            }

            if (VP.Y + VP.HEIGHT > worldSize.height - FIELD_SIDE_SIZE) {
                console.log(VP.HEIGHT - (VP.Y + VP.HEIGHT - (worldSize.height - FIELD_SIDE_SIZE)));
                if ((VP.HEIGHT - (VP.Y + VP.HEIGHT - (worldSize.height - FIELD_SIDE_SIZE))) / FIELD_SIDE_SIZE > Math.floor(height_fields)) {
                    y_max = Math.ceil(height_fields);
                }
            }

            for (let y = 0; y <= y_max; y++) {
                for (let x = 0; x <= x_max; x++) {
                    let x_pix = x * FIELD_SIDE_SIZE - VP.X % FIELD_SIDE_SIZE;
                    let y_pix = y * FIELD_SIDE_SIZE - VP.Y % FIELD_SIDE_SIZE;
                    let x_grid = x + Math.floor(VP.X / FIELD_SIDE_SIZE);
                    let y_grid = y + Math.floor(VP.Y / FIELD_SIDE_SIZE);
                    
                    let tile = tiles[worldGrid[y_grid][x_grid]];

                    context.drawImage(tile, x_pix, y_pix, FIELD_SIDE_SIZE, FIELD_SIDE_SIZE);
                };
            };

            // draw blobs
            drawBlobs(context, blobs, blob_images, player);

            // draw player
            drawPlayer(context, VP, player, 'rgba(255, 0, 0, 1)', player_colliding);



        },

    };

    var Player = function(game, VP, playerInfo, keyboarder) {
        this.game = game; // saved for later use
        this.size = { x: PLAYER_SIZE, y: PLAYER_SIZE };
        this.x = playerInfo.x;
        this.y = playerInfo.y;
        this.keyboarder = new Keyboarder();
    };


    var Keyboarder = function() {
        var keyState = {};

        window.onkeydown = function(e) {
            keyState[e.keyCode] = true;
        };

        window.onkeyup = function(e) {
            keyState[e.keyCode] = false;
        };

        this.isDown = function(e) {
            return keyState[keyCode] === true;
        };

        this.KEYS = { LEFT: 37, RIGHT: 39, UP: 38, DOWN: 40, SPACE: 32};
    };


    var drawBlobs = function(context, blobs, blob_images, player) {
        let player_x = player.x - VP.X;
        let player_y = player.y - VP.Y;

        let blob_colliding_with_player = false;
        blobs.forEach(function(one_blob) {
            let blob = one_blob.fields;
            let blob_colliding = {}
            blob_colliding.x = blob.x * FIELD_SIDE_SIZE + FIELD_SIDE_SIZE / 2 - BLOB_SIZE / 2;
            blob_colliding.y = blob.y  * FIELD_SIDE_SIZE + FIELD_SIDE_SIZE / 2  - BLOB_SIZE / 2;

            let x_pix = blob_colliding.x - VP.X;
            let y_pix = blob_colliding.y - VP.Y;
            if (x_pix + BLOB_SIZE < 0 || 
                x_pix > VP.WIDTH || 
                y_pix + BLOB_SIZE < 0 || 
                y_pix > VP.HEIGHT) { 
                return;
            }

            let blob_image = blob_images[blob.stage];
            console.log('player x', player_x);
            console.log('player y', player_y);
            console.log('blob x', blob_colliding.x);
            console.log('blob y', blob_colliding.y);
            if (colliding(blob_colliding, BLOB_SIZE, player, PLAYER_SIZE)) {
                blob_colliding_with_player = true;
            }
            context.drawImage(blob_image, x_pix, y_pix, BLOB_SIZE, BLOB_SIZE);

        });
        if (blob_colliding_with_player == true) {
            player_colliding = true;
        } else {
            player_colliding = false;
        }

    }


    var drawPlayer = function(context, VP, body, fillstyle, player_colliding) {
        context.fillStyle = fillstyle;

        if (player_colliding == true) {
            context.save();
            context.globalAlpha = 0.5;
            context.fillRect(body.x - VP.X,
                             body.y - VP.Y,
                             body.size.x, body.size.y);
            context.restore();
        } else {
            context.fillRect(body.x - VP.X,
                     body.y - VP.Y,
                     body.size.x, body.size.y);
        }


        //context.fillRect((playerX-vX)*32, (playerY-vY)*32, 32, 32);

    };
            

    var colliding = function(b1, b1_size, b2, b2_size) {
        return !(b1 == b2 ||
                 b1.x + b1_size <= b2.x ||
                 b1.y + b1_size <= b2.y ||
                 b1.x >= b2.x + b2_size ||
                 b1.y >= b2.y + b2_size);

    };

    window.onload = function() {
        new Game("canvas");
    };

};

