'''
File to help with turtlebot3.py environment.

'''

import time
import numpy as np
import pybullet as p
from collections import namedtuple

STATIC_MASS = 0
NULL_ID = -1
CLIENT = 0

# RGB colors
RGBA = namedtuple('RGBA', ['red', 'green', 'blue', 'alpha'])
RED = RGBA(1, 0, 0, 1)
GREEN = RGBA(0, 1, 0, 1)
BLUE = RGBA(0, 0, 1, 1)
BLACK = RGBA(0, 0, 0, 1)
WHITE = RGBA(1, 1, 1, 1)
YELLOW = RGBA(1, 1, 0, 1)
GREY = RGBA(0.5, 0.5, 0.5, 1)

JointInfo = namedtuple('JointInfo', ['jointIndex', 'jointName', 'jointType',
                                     'qIndex', 'uIndex', 'flags',
                                     'jointDamping', 'jointFriction', 'jointLowerLimit', 'jointUpperLimit',
                                     'jointMaxForce', 'jointMaxVelocity', 'linkName', 'jointAxis',
                                     'parentFramePos', 'parentFrameOrn', 'parentIndex'])


def Point(x=0., y=0., z=0.):
    return np.array([x, y, z])


def euler_from_quat(quat):
    return p.getEulerFromQuaternion(quat)  # rotation around fixed axis


def quat_from_euler(euler):
    return p.getQuaternionFromEuler(euler)


def get_pose(body):
    return p.getBasePositionAndOrientation(body, physicsClientId=CLIENT)
    # return np.concatenate([point, quat])


def get_point(body):
    return get_pose(body)[0]


def get_quat(body):
    return get_pose(body)[1]  # [x,y,z,w]


def get_euler(body):
    return euler_from_quat(get_quat(body))


def set_pose(body, pose):
    (point, quat) = pose
    p.resetBasePositionAndOrientation(body, point, quat)


def set_point(body, point):
    quat = p.getBasePositionAndOrientation(body)[1]
    set_pose(body, (point, quat))


def set_quat(body, quat):
    set_pose(body, (get_point(body), quat))


def set_euler(body, euler):
    set_quat(body, quat_from_euler(euler))


def unit_point():
    return (0., 0., 0.)


def unit_quat():
    return quat_from_euler([0, 0, 0])  # [X,Y,Z,W]


def unit_pose():
    return (unit_point(), unit_quat())


def get_box_geometry(width, length, height):
    return {
        'shapeType': p.GEOM_BOX,
        'halfExtents': [width / 2., length / 2., height / 2.]
    }


def get_sphere_geometry(radius):
    return {
        'shapeType': p.GEOM_SPHERE,
        'radius': radius,
    }


def get_joint_info(body, joint):
    return JointInfo(*p.getJointInfo(body, joint, physicsClientId=CLIENT))


def get_joint_name(body, joint):
    return get_joint_info(body, joint).jointName.decode('UTF-8')


def joint_from_name(body, name):
    num_joints = p.getNumJoints(body, physicsClientId=CLIENT)
    joint_list = list(range(num_joints))
    for joint in joint_list:
        if get_joint_name(body, joint) == name:
            return joint
    raise ValueError(body, name)


def joints_from_names(body, names):
    return tuple(joint_from_name(body, name) for name in names)


def set_joint_positions(body, joints, values):
    for joint, value in zip(joints, values):
        p.resetJointState(body, joint, targetValue=value, targetVelocity=0, physicsClientId=CLIENT)


def set_preview(enable):
    # lightPosition, shadowMapResolution, shadowMapWorldSize
    p.configureDebugVisualizer(p.COV_ENABLE_GUI, enable, physicsClientId=CLIENT)
    p.configureDebugVisualizer(p.COV_ENABLE_RGB_BUFFER_PREVIEW, enable, physicsClientId=CLIENT)
    p.configureDebugVisualizer(p.COV_ENABLE_DEPTH_BUFFER_PREVIEW, enable, physicsClientId=CLIENT)
    p.configureDebugVisualizer(p.COV_ENABLE_SEGMENTATION_MARK_PREVIEW, enable, physicsClientId=CLIENT)
    #p.configureDebugVisualizer(p.COV_ENABLE_WIREFRAME, True, physicsClientId=CLIENT)


def create_collision_shape(geometry, pose=unit_pose()):
    point, quat = pose
    collision_args = {
        'collisionFramePosition': point,
        'collisionFrameOrientation': quat,
        'physicsClientId': CLIENT
    }
    collision_args.update(geometry)
    if 'length' in collision_args:
        collision_args['height'] = collision_args['length']
        del collision_args['length']
    return p.createCollisionShape(**collision_args)


def create_visual_shape(geometry, pose=unit_pose(), color=RED, specular=None):
    if (color is None):  # or not has_gui():
        return NULL_ID
    point, quat = pose
    visual_args = {
        'rgbaColor': color,
        'visualFramePosition': point,
        'visualFrameOrientation': quat,
        'physicsClientId': CLIENT,
    }
    visual_args.update(geometry)
    if specular is not None:
        visual_args['specularColor'] = specular
    return p.createVisualShape(**visual_args)


def create_shape(geometry, pose=unit_pose(), collision=True, **kwargs):
    collision_id = create_collision_shape(geometry, pose=pose) if collision else NULL_ID
    visual_id = create_visual_shape(geometry, pose=pose, **kwargs)  # if collision else NULL_ID
    return collision_id, visual_id


def create_body(collision_id=NULL_ID, visual_id=NULL_ID, mass=STATIC_MASS):
    return p.createMultiBody(baseMass=mass, baseCollisionShapeIndex=collision_id,
                             baseVisualShapeIndex=visual_id, physicsClientId=CLIENT)


def create_box(w, l, h, mass=STATIC_MASS, color=RED, **kwargs):
    collision_id, visual_id = create_shape(get_box_geometry(w, l, h), color=color, **kwargs)
    return create_body(collision_id, visual_id, mass=mass)


def create_sphere(radius, mass=STATIC_MASS, color=BLUE, **kwargs):
    collision_id, visual_id = create_shape(get_sphere_geometry(radius), color=color, **kwargs)
    return create_body(collision_id, visual_id, mass=mass)


def change_color(body, color):
    joints_num = p.getNumJoints(body)
    print(joints_num)
    for joint in range(joints_num):
        joint_info = JointInfo(*p.getJointInfo(body, joint))
        if joint_info.jointType == p.JOINT_REVOLUTE:
            p.changeVisualShape(body, joint, rgbaColor=color)


# HELPER FUNCTIONS
def elapsed_time(start_time):
    return time.time() - start_time


def wait_for_duration(duration):
    t0 = time.time()
    MouseEvent = namedtuple('MouseEvent', ['eventType', 'mousePosX', 'mousePosY', 'buttonIndex', 'buttonState'])
    while elapsed_time(t0) <= duration:
        list(MouseEvent(*event) for event in p.getMouseEvents(physicsClientId=CLIENT))


def is_overlapping(vertices1, vertices2):
    """
    Checking if two polygons are overlapping using separate axis theorem (SAT)
    a vertex has form (x,y)
    :param vertices1: list of vertices in the first polygon
    :param vertices2: list of vertices in the second polygon
    :return: True if two polygons overlap, False otherwise
    """
    for polygon in [vertices1, vertices2]:
        for i in range(len(polygon)):
            v1 = polygon[i]
            v2 = polygon[(i + 1) % len(polygon)]
            normal_vector = [v2[1] - v1[1], v1[0] - v2[0]]
            normal_vector = normal_vector / np.linalg.norm(normal_vector)  # normalize

            projections1 = [np.dot(vertex, normal_vector) for vertex in vertices1]
            min1, max1 = [min(projections1), max(projections1)]
            projections2 = [np.dot(vertex, normal_vector) for vertex in vertices2]
            min2, max2 = [min(projections2), max(projections2)]

            if max1 < min2 or max2 < min1:
                return False

    return True
