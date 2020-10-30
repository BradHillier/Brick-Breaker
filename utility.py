import pygame
from settings import BALL_SPEED
from math import sqrt


def collision_helper_AABB(stationary, moving):
    """
    Calculates which side of a stationary object a moving
    object collided with using axis-aligned bounding box collision detection.
    """
    corner_slope_rise = 0
    corner_slope_run = 0    # TODO somestimes causes a division by zero
    # Lazy way to avoid division by zero
    try:
        velocity_slope = moving.dy / moving.dx
    except:
        velocity_slope = moving.dy / 0.0001
    potential_collision_side = set()

    if moving.prev.right <= stationary.rect.left:
        # Did not collide right; might have collided left
        potential_collision_side.add('left')
        corner_slope_run = stationary.rect.left - moving.prev.right
        if moving.prev.bottom <= stationary.rect.top:
            potential_collision_side.add('top')
            corner_slope_rise = stationary.rect.top - moving.prev.bottom
        elif moving.prev.top >= stationary.rect.bottom:
            potential_collision_side.add('bottom')
            corner_slope_rise = stationary.rect.bottom - moving.prev.top
        else:
            return 'left'
    elif moving.prev.left >= stationary.rect.right:
        # Did not collide left; might have collided right
        potential_collision_side.add('right')
        corner_slope_run = moving.prev.left - stationary.rect.right
        if moving.prev.bottom <= stationary.rect.top:
            potential_collision_side.add('top')
            corner_slope_rise = moving.prev.bottom = stationary.rect.top
        elif moving.prev.top >= stationary.rect.bottom:
            potential_collision_side.add('bottom')
            corner_slope_rise = moving.prev.top = stationary.rect.bottom
        else:
            return 'right'
    else:
        # Did not collide with either left or right side
        if moving.prev.bottom <= stationary.rect.top:
            return 'top'
        elif moving.prev.top >= stationary.rect.bottom:
            return 'bottom'
        else:
            print('NONE')
    if corner_slope_run == 0: corner_slope_run = 0.000001
    # Corner case; Might have collided with more than one side
    return collision_from_slope(potential_collision_side, 
            velocity_slope, corner_slope_rise / corner_slope_run)


def collision_from_slope(potential_collision_sides, 
                         velocity_slope, corner_slope):
    """
    determine which side of a stationary object was collided with by
    comparing the slope of the moving object's velocity and the slope of
    the velocity that would have caused the moving object to touch 
    corners with the stationary object.
    """
    if 'top' in potential_collision_sides:
        if 'left' in potential_collision_sides:
            return 'top' if velocity_slope < corner_slope else 'left'
        elif 'right' in potential_collision_sides:
            return 'top' if velocity_slope > corner_slope else 'right'
    elif 'bottom' in potential_collision_sides:
        if 'left' in potential_collision_sides:
            return 'bottom' if velocity_slope > corner_slope else 'left'
        elif 'right' in potential_collision_sides:
            return 'bottom' if velocity_slope < corner_slope else 'left'

def controlled_deflect(ball, player):
    """
    Deflect ball at an angle relative to the point of collisions
    distance from the center of the player
    """
    distance_from_center = ball.rect.centerx - player.rect.centerx
    max_collision_point = (player.rect.width / 2 + ball.rect.width / 2)
    percent_from_max = distance_from_center / max_collision_point
    # Avoid ball moving in a horizontal line
    dx = min(BALL_SPEED * percent_from_max, BALL_SPEED * 0.8)
    dy = -sqrt((BALL_SPEED**2 - dx**2))
    return pygame.math.Vector2(dx, dy)

