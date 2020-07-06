//Jacob Hopkins
// July-2020
//Simulation for Biology
//Predator Prey Simulation for collecting RAW data about predation
//Designed to look into the effects of prey spacial distributions
// and the effects of enviroment obstacle complexity.
//https://processing.org/reference/selectFolder_.html

//proccessing variables
let fps = 8
let version = '1.0'

//graphics variables, window
let window_background = 1
let win_w = 800
let win_h = 600


//graphics variables, hud
let hud_scale = 0.25
let hud_bezl = 25
let hud_offset = 5
let hud_background = 151
let hud_w = win_w * hud_scale
let hud_pos = win_w - hud_w


//graphics variables, sim
let sim_background = 51
let sim_scale = 1 - hud_scale
let sim_w = win_w * sim_scale

//background color variables
let obstacle_background = 1
let predator_background
let prey_background = 151
let selected = 101
let unselected = 151
let text_color = 0
let med_gray = 51
let light_gray = 151
let white = 255

//simulation variables, setup
let starting_prey_count = 100
let prey_count = starting_prey_count
let simulation_length = 60
let blindfold = true

//grid variables
let rows
let cell_size
let timer_text
let grid
let start
let count_down = 3
let prey_distribution = -1
let enviroment_complexity = -1

//ENUMS
let EMPTY = 0
let PREY = 1
let OBSTACLE = 2
let PREDATOR = 3

let UNDECIDED = -1

let EVEN = 0
let RANDOM = 1
let CLUMPED = 2

let SIMPLE = 0
let MODERATE = 1
let COMPLEX = 2

//variables for the player
let predator_x, predator_y

//variables for menu selection
let prey_dist_selection = [0, 0, 0]
let env_complexity_selection = [0, 0, 0]

var prey_dist_labels = ["EVEN", "RANDOM", "CLUMPED"]
var env_complexity_labels = ["SIMPLE", "MODERATE", "COMPLEX"]

//image for scsu
let img, img2


//proccessing functions
//this runs first. only once
function setup() {
  createCanvas(win_w, win_h)
  img = loadImage("biology_department_670b-1.jpg")
  img2 = loadImage("scsu.png")

  frameRate(fps)

  //create custom collor for predator
  predator_background = color(255, 0, 0)

  create_empty_grid()
  
  start = true

}

//after setup this function is repeated endless/until-stop
function draw() {
  background(window_background)

  if (prey_distribution == UNDECIDED && enviroment_complexity == UNDECIDED) {

    draw_selection_menu()
    check_for_pre_selection()

  } else {
    
    if (start){
      populate_grid()
      spawn_predator()
      start = false
    }
    
    draw_hud()
    draw_simulation()

    if (gametime() < simulation_length) { //remove controls from player when simulation stops
      controls()
    }else{
      end_sim_screen()
      check_for_post_selection()
    }

  }

}


//my functions

//this is the background and draw of the grid
function draw_simulation() {
  fill(sim_background)
  rect(0, 0, sim_w, win_h)

  for (var y = 0; y < rows; y++) {
    for (var x = 0; x < rows; x++) {
      if (grid[x][y] == EMPTY) {
        fill(sim_background)
      }
      if (grid[x][y] == PREY) {
        fill(prey_background)
        if(blindfold){
          fill(sim_background)
        }
        if(game_over()){
          fill(prey_background)
        }
      }
      if (grid[x][y] == OBSTACLE) {
        fill(obstacle_background)
      }
      if (grid[x][y] == PREDATOR) {
        fill(predator_background)
      }
      rect(x * cell_size, y * cell_size, cell_size, cell_size)
    }
  }
}



function draw_hud() {
  draw_hud_display()
  draw_hud_dialog()
}

function draw_hud_display() {
  fill(hud_background)
  rect(hud_pos + hud_offset, 0 + hud_offset, hud_w - 2 * hud_offset, win_h - 2 * hud_offset, hud_bezl)
  image(img, hud_pos + 2 * hud_offset, 30 * hud_offset, img.width / 2.2, img.height / 2)
  image(img2, hud_pos + 2 * hud_offset, 40 * hud_offset, img.width / 2.2, img.height)
}

function draw_hud_dialog() {
  fill(text_color)
  textSize(16)
  
  
  
  var s_prey_count_text = "Prey Count(START):" + starting_prey_count
  text(s_prey_count_text, hud_pos + 3 * hud_offset, 6 * hud_offset)
  
  var prey_dist_text = "Prey Dist.: " + prey_dist_labels[prey_distribution]
  text(prey_dist_text, hud_pos + 3 * hud_offset, 10 * hud_offset)
  
  var env_comp_text = "Env Comp.: " + env_complexity_labels[enviroment_complexity]
  text(env_comp_text, hud_pos + 3 * hud_offset, 14 * hud_offset)
  
  if (gametime() <= simulation_length) { //only update the timer text if the timer is within game time
    timer_text = "Time (seconds):" + gametime() + "s"
  }
  text(timer_text, hud_pos + 3 * hud_offset, 18 * hud_offset)
  
  let prey_count_text = "Prey Count(ALIVE):" + prey_count
  text(prey_count_text, hud_pos + 3 * hud_offset, 22 * hud_offset)
  
  let dead_prey_count_text = "Prey Count(DEAD):" + (starting_prey_count - prey_count)
  text(dead_prey_count_text, hud_pos + 3 * hud_offset, 26 * hud_offset)
  
  let controls_text = "Controls:"
  text(controls_text, hud_pos + 3 * hud_offset, 62 * hud_offset)
  
  let up_control_text = " Up:     W | ^"
  text(up_control_text, hud_pos + 3 * hud_offset, 66 * hud_offset)
  
  let down_control_text = " Down: S | v"
  text(down_control_text, hud_pos + 3 * hud_offset, 69 * hud_offset)
  
  let left_control_text = " Left:    A | <"
  text(left_control_text, hud_pos + 3 * hud_offset, 72 * hud_offset)
  
  let right_control_text = " Right:  D | >"
  text(right_control_text, hud_pos + 3 * hud_offset, 75 * hud_offset)
  
  let stop_clock_control_text = " End Simulation:  Esc"
  text(stop_clock_control_text, hud_pos + 3 * hud_offset, 78 * hud_offset)
}



function draw_selection_menu() {
  var offset = 50
  fill(med_gray)
  rect(offset, offset, win_w - 2 * offset, win_h - 2 * offset)

  fill(text_color)
  textSize(16)
  text("Prey Distributions", 2 * offset, 1.8 * offset)
  text("Enviroment Complexities", 2 * offset, 5.8 * offset)

  for (var i = 0; i < 3; i++) {
    
    if (prey_dist_selection[i] == 1) { fill(selected) } else { fill(unselected) }
    rect(2 * offset + i * 4 * offset, 2 * offset, 4 * offset, 3 * offset)
    
    if (env_complexity_selection[i] == 1) { fill(selected) } else { fill(unselected) }
    rect(2 * offset + i * 4 * offset, 6 * offset, 4 * offset, 3 * offset)
    
    fill(text_color)
    text(prey_dist_labels[i], 3.4 * offset + i * 4 * offset, 3.5 * offset)
    text(env_complexity_labels[i], 3.4 * offset + i * 4 * offset, 7.5 * offset)
  }

  fill(light_gray)
  rect(6 * offset, 9.5 * offset, 4 * offset, offset)
  if (blindfold) { fill(selected) } else { fill(unselected) }
  rect(3 * offset, 9.6 * offset, 2 * offset, 0.8 * offset)
  fill(text_color)
  textSize(16)
  text("Start", 7.6 * offset, 10.1 * offset)
  text("BLINDFOLD", 3.1 * offset, 10.1 * offset)
  
  
}

function check_for_pre_selection() {

  var offset = 50

  if (mouseIsPressed) {

    for (var i = 0; i < 3; i++) {
      var start_X = 2 * offset + i * 4 * offset
      var box_width = 4 * offset, box_height = 3 * offset
      if (mouseX > start_X && mouseX < start_X + box_width) {
        
        if(mouseY > 2 * offset && mouseY < 2 * offset + box_height){
          prey_dist_selection = [UNDECIDED,UNDECIDED,UNDECIDED]
          prey_dist_selection[i] = 1
        }
        if(mouseY > 6 * offset && mouseY < 6 * offset + box_height){
          env_complexity_selection = [UNDECIDED,UNDECIDED,UNDECIDED] 
          env_complexity_selection[i] = 1
        }
        break
      }
    }
    if(mouseX > 3 * offset && mouseX < 3 * offset + 2 * offset){
       if(mouseY > 9.6 * offset && mouseY < 9.6 * offset + 0.8 * offset){
         blindfold = !blindfold
      }
    }
      
    if (mouseX > 6 * offset && mouseX < 6 * offset + 4 * offset){
      if (mouseY > 9.5 * offset && mouseY < 9.5 * offset + offset){
        fill(selected)
        rect(6 * offset, 9.5 * offset, 4 * offset, offset)
        fill(text_color)
        textSize(16)
        text("Start", 7.6 * offset, 10.1 * offset)
        for(var j = 0; j < 3; j++){
          if(prey_dist_selection[j] != UNDECIDED && prey_distribution == UNDECIDED){
            prey_distribution = j
          }
          if(env_complexity_selection[j] != UNDECIDED && enviroment_complexity == UNDECIDED){
            enviroment_complexity = j
          }
        }
      }
    }

  }

}
  

function end_sim_screen(){
  //background
  fill(med_gray)
  var height = (win_h - 2 * hud_offset)/4
  rect(hud_pos + 3 * hud_offset, win_h - 4 * hud_offset - height, hud_w - 6 * hud_offset, height, hud_bezl)
  
  //text above
  fill(text_color)
  text("Simulation Complete", hud_pos + 4.5 * hud_offset, win_h - 5 * hud_offset - height)
  
  //3 boxes
  fill(light_gray)
  rect(hud_pos + 3.5 * hud_offset, win_h - 4 * hud_offset - height, hud_w - 7 * hud_offset, height/3, hud_bezl)
  rect(hud_pos + 3.5 * hud_offset, win_h - 4 * hud_offset - height + height/3, hud_w - 7 * hud_offset, height/3, hud_bezl)
  rect(hud_pos + 3.5 * hud_offset, win_h - 4 * hud_offset - height + 2 * height/3, hud_w - 7 * hud_offset, height/3, hud_bezl)
  
  //text in boxes
  fill(text_color)
  text("Restart",hud_pos + 5 * hud_offset, win_h + 2 * hud_offset - height)
  text("Save Screenshot", hud_pos + 5 * hud_offset, win_h + 2 * hud_offset - height + height/3)
  text("Save Results", hud_pos + 5 * hud_offset, win_h + 2 * hud_offset - height + 2 * height/3)
}

function check_for_post_selection(){
  var height = (win_h - 2 * hud_offset)/4
  if (mouseIsPressed) {
    
    if(mouseX > hud_pos + 3.5 * hud_offset && mouseX < hud_pos + 3.5 * hud_offset + hud_w - 7 * hud_offset){
      if(mouseY > win_h - 4 * hud_offset - height && mouseY < win_h - 4 * hud_offset - height + height/3){
        let onClick = window.location.reload()
      }
    
      if(mouseY > win_h - 4 * hud_offset - height + height/3 && mouseY < win_h - 4 * hud_offset - height + 2 * height/3){
        save("PredatorPreySimulation_"+prey_dist_labels[prey_distribution]+"_"+env_complexity_labels[enviroment_complexity]+".jpg")
      }
      
      if(mouseY > win_h - 4 * hud_offset - height + 2 * height/3 && mouseY < win_h - 4 * hud_offset){
        var spacer = ""       
        var title = "Predator Prey Simulation " + version
        var date = "Date Simulated: " + day() + "-" + month() + "-" + year()
        var time = "Time Simulated: " + hour() + ":" + minute()
        var run_time = "Simulation Length: " + simulation_length + " seconds"
        var prey_dist = "Prey Distribution: " + prey_dist_labels[prey_distribution]
        var env_comp = "Enviroment Complexity: " + env_complexity_labels[enviroment_complexity]
        var prey_total = "Starting Prey Count: " + starting_prey_count
        var prey_alive = "Surviving Prey Count: " + prey_count
        var prey_dead = "Prey Touched/Killed: " + (starting_prey_count - prey_count)
        var blindfold = "Blindfold: " + (blindfold == false)
        
        let array_for_file = [title, date, time, spacer, run_time, spacer, blindfold, spacer, prey_dist, spacer, env_comp, spacer, prey_total, prey_alive, spacer, prey_dead]
        
          saveStrings(array_for_file, "PredatorPreySimulation_"+prey_dist_labels[prey_distribution]+"_"+env_complexity_labels[enviroment_complexity]+".txt")
      }
      
    }
  }
}
  
function controls() {
  //https://keycode.info/
  if (keyIsDown(UP_ARROW) || keyIsDown(87)) { //w == 87
    predator_attempt_move(predator_x, predator_y - 1)
  } else if (keyIsDown(DOWN_ARROW) || keyIsDown(83)) { //s == 83
    predator_attempt_move(predator_x, predator_y + 1)
  } else if (keyIsDown(LEFT_ARROW) || keyIsDown(65)) { //a == 65
    predator_attempt_move(predator_x - 1, predator_y)
  } else if (keyIsDown(RIGHT_ARROW) || keyIsDown(68)) { //d == 68
    predator_attempt_move(predator_x + 1, predator_y)
  }else if (keyIsDown(ESCAPE)) { //d == 68
    frameCount = fps * 60
  }
}
  
  

function create_empty_grid() {
  
  //size of the grid is decided and 
  rows = round(2 * sqrt(starting_prey_count) + 1)
  cell_size = sim_w / rows

  //create the grid array
  grid = new Array(rows)

  //make it 2d
  for (var n = 0; n < grid.length; n++) {
    grid[n] = new Array(rows)
  }

  //populate it with 0s
  for (var i = 0; i < grid.length; i++) {
    for (var j = 0; j < grid[i].length; j++) {
      grid[i][j] = EMPTY
    }
  }

}
  
function populate_grid(){
  populate_prey()
  populate_obstacles()
}


function populate_prey(){
  
  if(prey_distribution == EVEN){
    var spawned = 0
    for(var y = 0; y < rows/2 - 1; y++){
      for(var x = 0; x < rows/2 - 1; x++){
        var spaced_x = 2 * x + 1
        var spaced_y = 2 * y + 1
        grid[spaced_x][spaced_y] = PREY
        spawned++
      }
    }
    spawn_prey_random_location(starting_prey_count - spawned)
  }
  
  if(prey_distribution == RANDOM){
    spawn_prey_random_location(starting_prey_count)
  }
  
  if(prey_distribution == CLUMPED){
    var clusters = 0, cluster_size = 4
    var remainder_prey = starting_prey_count%cluster_size
    while(cluster_size * clusters != starting_prey_count - remainder_prey){
      var rand_start_x = int(random(rows - 1))
      var rand_start_y = int(random(rows - 1))
      
      var top_left = grid[rand_start_x][rand_start_y] == EMPTY
      var top_right =  grid[rand_start_x + 1][rand_start_y] == EMPTY
      var bottom_left = grid[rand_start_x][rand_start_y + 1] == EMPTY
      var bottom_right = grid[rand_start_x + 1][rand_start_y + 1] == EMPTY
      
      if (top_left && top_right && bottom_left && bottom_right ){
        grid[rand_start_x][rand_start_y] = PREY
        grid[rand_start_x + 1][rand_start_y] = PREY
        grid[rand_start_x][rand_start_y + 1] = PREY
        grid[rand_start_x + 1][rand_start_y + 1] = PREY
        clusters++
      }
    }
    
    spawn_prey_random_location(remainder_prey)
     
  }
  
}
  
function spawn_prey_random_location(to_spawn){
  var spawned = 0
  while(spawned < to_spawn){
    var rand_x = int(random(rows))
    var rand_y = int(random(rows))
    if (grid[rand_x][rand_y] == EMPTY){
      grid[rand_x][rand_y] = PREY
      spawned++
    }
  }
}
  
function populate_obstacles(){
  
  var obstacle_count = 6
  var direction = false
  
  if(enviroment_complexity == MODERATE){
    while(obstacle_count > 0){
      
      spawn_obstacle(4, direction)
      spawn_obstacle(2, direction)
      direction = !direction
      obstacle_count -= 2
    }
  }
  
  if(enviroment_complexity == COMPLEX){
    obstacle_count = obstacle_count * 2
    while(obstacle_count > 0){
      spawn_obstacle(4, direction)
      spawn_obstacle(2, direction)
      direction = !direction
      obstacle_count -= 2
    }
  }
  
}

function spawn_obstacle(size, direction){//true for right, false for down
  var placed = false
  while(!placed){
    var rand_start_x = int(random(rows - size))
    var rand_start_y = int(random(rows - size))
    
    var right = 0, down = 0
    for (var l = 0; l < size; l++){   
      if(direction){
        if(grid[rand_start_x+l][rand_start_y] == EMPTY){
           right++
        }
      }else{
        if(grid[rand_start_x][rand_start_y+l] == EMPTY){
           down++
        }
      }
    }
    
    if(direction){
      if(right == size){
         for(var p = 0; p < size; p++){
           grid[rand_start_x+p][rand_start_y] = OBSTACLE
           placed = true
         }
      }
    }else{
      if(down == size){
         for(var q = 0; q < size; q++){
           grid[rand_start_x][rand_start_y+q] = OBSTACLE
           placed = true
         }
      }
    }
  }
}


function spawn_predator() {
  //spawn the predator randomly
  var spawned = true
  while (spawned){
    predator_x = int(random(rows))
    predator_y = int(random(rows))
    if (grid[predator_x][predator_y] == EMPTY){
      grid[predator_x][predator_y] = PREDATOR
      spawned = false
    }
  }
  
}

function predator_attempt_move(x, y) {
  if (predator_can_move(x, y)) {
    predator_move(x, y)
    return 1
  }
  return -1
}

function predator_can_move(x, y) {
  if (x > -1 && x < rows) {
    if (y > -1 && y < rows) {
      if (grid[x][y] < OBSTACLE) {
        return true
      }
    }
  }
  return false
}

function predator_move(x, y) {
  if (grid[x][y] == PREY) {
    prey_count--
  }
  grid[predator_x][predator_y] = EMPTY
  predator_x = x
  predator_y = y
  grid[predator_x][predator_y] = PREDATOR

}


function gametime() {
  return round(frameCount / fps);
}
  
function game_over(){
  return gametime() >= simulation_length
}