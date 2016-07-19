"use strict";

var init_canvas = function(world_object, blobs) {

    console.log(world_object);


    var canvas, context, viewportSize;

    // viewport

    var VP = { X: 0, 
               Y: 0, 
               WIDTH: 20 * 40 ,    // keep this one divisable by the speed for now. Default: 512
               HEIGHT: 20 * 15 };  // keep this one divisable by by the speed for now. Default: 352

    const FIELD_SIDE_SIZE = 32;

    const NUM_OF_TILES = 2;

    const NUM_OF_BLOBS = 1;

    const BLOB_SIZE = 9;

    const PLAYER_SIZE = 16;

    const world = world_object[0].fields;

    // console.log('blobs ' + blobs.1.x );

    // var blobs = [];

    // let blobs_object = {{ blobs }};

    /*
    blobs_object.forEach(function(blob) {
        console.log(blob);
        let blob_parsed = { x: blob.x,
                     y: blob.y
                     type: stage
                   };
        blobs.push(blob_parsed);
    }
    */


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
                if (player.position.x > 0) player.position.x -= 16;
            }

            if (key == 38) {
                // Up
                if (player.position.y > 0) player.position.y -= 16;
            }

            if (key == 39) {
                // Right
                if (player.position.x < (worldSize.width - player.size.x)) player.position.x += 16;
            }

            if (key == 40) {
                // Down
                if (player.position.y < (worldSize.height - player.size.y)) player.position.y += 16;
            }
            // Okay! The player is done moving, now we have to determine the "best" viewport.
            // Ideally the viewport centers the player,
            // but if its too close to an edge we'll have to deal with that edge

            VP.X = player.position.x - Math.floor(0.5 * VP.WIDTH);
            if (VP.X < 0) VP.X = 0;
            if (VP.X + VP.WIDTH > worldSize.width) VP.X = worldSize.width - VP.WIDTH;          
            
            VP.Y = player.position.y - Math.floor(0.5 * VP.HEIGHT);
            if (VP.Y < 0) VP.Y = 0;
            if (VP.Y + VP.HEIGHT > worldSize.height) VP.Y = worldSize.height - VP.HEIGHT;
            //console.log("VP y" + VP.Y);
            //Game.draw(context, VP, worldGrid, worldSize, tiles, blob_images, blobs, player);

            //let y_grid = Math.floor(VP.Y / FIELD_SIDE_SIZE);
            //let x_grid = Math.floor(VP.X / FIELD_SIDE_SIZE);

            //console.log(y_grid);
            //console.log(x_grid);
            //console.log(player.position.y);
            //console.log(worldSize.height);
            //console.log(worldSize.y);
            //console.log(player.position.x);
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

            blobs.forEach(function(blob) {
                console.log( blob.fields);
                let blob_properties = blob.fields;
                let x_pix = blob_properties.x * FIELD_SIDE_SIZE + FIELD_SIDE_SIZE / 2;
                let y_pix = blob_properties.y * FIELD_SIDE_SIZE + FIELD_SIDE_SIZE / 2;
                if (x_pix + BLOB_SIZE < VP.X || 
                    x_pix > VP.X + VP.WIDTH || 
                    y_pix + BLOB_SIZE < VP.Y || 
                    y_pix > VP.Y + VP.HEIGHT) { 
                    return;
                }

                let blob_image = blob_images[blob_properties.stage];
                context.drawImage(blob_image, x_pix, y_pix, BLOB_SIZE, BLOB_SIZE);

            });

            // draw blobs
            drawBlobs(context, blobs, blob_images);

            // draw player
            drawPlayer(context, VP, player, 'rgba(255, 0, 0, 0.5)');


        },

    };

    var Player = function(game, VP, playerInfo, keyboarder) {
        this.game = game; // saved for later use
        this.size = { x: PLAYER_SIZE, y: PLAYER_SIZE };
        this.position = { x: playerInfo.x, y: playerInfo.y };
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


    var drawBlobs = function(context, blobs, blob_images) {
        blobs.forEach(function(blob) {
            console.log( blob.fields);
            let blob_properties = blob.fields;
            let x_pix = blob_properties.x * FIELD_SIDE_SIZE + FIELD_SIDE_SIZE / 2;
            let y_pix = blob_properties.y * FIELD_SIDE_SIZE + FIELD_SIDE_SIZE / 2;
            if (x_pix + BLOB_SIZE < VP.X || 
                x_pix > VP.X + VP.WIDTH || 
                y_pix + BLOB_SIZE < VP.Y || 
                y_pix > VP.Y + VP.HEIGHT) { 
                return;
            }

            let blob_image = blob_images[blob_properties.stage];
            context.drawImage(blob_image, x_pix, y_pix, BLOB_SIZE, BLOB_SIZE);

        });

    }


    var drawPlayer = function(context, VP, body, fillstyle) {
        context.fillStyle = fillstyle;
        context.fillRect(body.position.x - VP.X,
                         body.position.y - VP.Y,
                         body.size.x, body.size.y);

        //context.fillRect((playerX-vX)*32, (playerY-vY)*32, 32, 32);

    };
            



    console.log('hi');


    window.onload = function() {
        new Game("canvas");
    };

};

