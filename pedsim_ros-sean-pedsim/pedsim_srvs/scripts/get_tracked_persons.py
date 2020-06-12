#!/usr/bin/env python

#this service will listen to the msgs from visualizer to get agents
#positions. Then at service request will return a list of positions
#for given agent ids.

from pedsim_srvs.srv import GetAgentPos, GetAgentPosResponse
from pedsim_msgs.msg import TrackedPersons
from geometry_msgs.msg import Point
import rospy

tp = None

def poseCallback(data):
    global tp 
    tp = data

def handle_get_all_persons(req):
    print "returning agent states "
    pos_array = []
    pos = Point()
    if tp is not None:
        for i in req.agent_ids:
            pos = tp.tracks[i].pose.pose.position
            pos_array.append(pos)
    return GetAgentPosResponse(pos_array)


def get_all_tracked_persons_server():
    #rospy.init_node('get_all_tracked_persons_server')
    s = rospy.Service('get_all_tracked_persons', GetAgentPos,
    handle_get_all_persons)
    print "ready to get agent states"
    #rospy.spin()

def tracked_persons_listener():
    #rospy.init_node('tracked persons listener')
    l = rospy.Subscriber('/pedsim_visualizer/tracked_persons', TrackedPersons,
    poseCallback)
    print "listening to agent states"


if __name__ == "__main__":
    rospy.init_node('tracked_persons_utils')
    get_all_tracked_persons_server()
    tracked_persons_listener()
    rospy.spin()
