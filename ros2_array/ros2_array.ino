#include <micro_ros_arduino.h>
#include <stdio.h>
#include <rcl/rcl.h>
#include <rcl/error_handling.h>
#include <std_msgs/msg/int32_multi_array.h>
#include <std_msgs/msg/multi_array_dimension.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>

#define BUFFER_SIZE 4
#define STRING_SIZE 10
#define POT0_PIN 4
#define POT1_PIN 15
#define POT2_PIN 12
#define POT3_PIN 13

#define RCCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){printf("Failed status on line %d: %d. Aborting.\n",__LINE__,(int)temp_rc);vTaskDelete(NULL);}}
#define RCSOFTCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){printf("Failed status on line %d: %d. Continuing.\n",__LINE__,(int)temp_rc);}}

rcl_publisher_t publisher;
std_msgs__msg__Int32MultiArray msg;
rclc_executor_t executor;
rcl_allocator_t allocator;
rclc_support_t support;
rcl_node_t node;
rcl_timer_t timer;

#define LED_PIN 2

void error_loop(){
  while(1){
    digitalWrite(LED_PIN, !digitalRead(LED_PIN));
    delay(100);
  }
}

void timer_callback(rcl_timer_t * timer, int64_t last_call_time)
{
	RCLC_UNUSED(last_call_time);
	if (timer != NULL) {
		RCSOFTCHECK(rcl_publish(&publisher, &msg, NULL));
		//(void)! rcl_publish(&publisher, &msg, NULL)
	}
}

void setup()
{
  set_microros_transports();
  
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, HIGH);  
  
  delay(2000);

  allocator = rcl_get_default_allocator();

	// create init_options
	RCCHECK(rclc_support_init(&support, 0, NULL, &allocator));

	// create node
	RCCHECK(rclc_node_init_default(&node, "int32_array_publisher", "", &support));

	// create publisher
	RCCHECK(rclc_publisher_init_default(
		&publisher,
		&node,
		ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32MultiArray),
		"pot_topic"));

	// create timer,
	const unsigned int timer_timeout = 100;
	RCCHECK(rclc_timer_init_default(
		&timer,
		&support,
		RCL_MS_TO_NS(timer_timeout),
		timer_callback));

	// create executor
	RCCHECK(rclc_executor_init(&executor, &support.context, 1, &allocator));
	RCCHECK(rclc_executor_add_timer(&executor, &timer));
	
  //init mess
  {
    static int32_t buffer[BUFFER_SIZE] = {};
    msg.data.data = buffer;
    msg.data.size = 0;
    msg.data.capacity = BUFFER_SIZE;

    static std_msgs__msg__MultiArrayDimension dim[1] = {};
    msg.layout.dim.data = dim;
    msg.layout.dim.size = 0;
    msg.layout.dim.capacity = 1;

    static char labels[1][STRING_SIZE] = {};	
    msg.layout.dim.data[0].label.data = labels[0];
    msg.layout.dim.data[0].label.size = 0;
    msg.layout.dim.data[0].label.capacity = STRING_SIZE;
	}		
}

void loop() {
  msg.data.data[0]= analogRead(POT0_PIN);
  msg.data.data[1]= analogRead(POT1_PIN);
  msg.data.data[2]= analogRead(POT2_PIN);
  msg.data.data[3]= analogRead(POT3_PIN);
  msg.data.size = 4;

  RCSOFTCHECK(rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100)));
}