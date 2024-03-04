


function R = calculateRotationMatrix(pitch, roll)
    
    % calculate the rotation matrix for a pitch + roll movement
    % rotation about y is pitch, and rotation about x is roll

    R_pitch = [cosd(pitch) 0 sind(pitch); 0 1 0; -sind(pitch) 0 cosd(pitch)];
    R_roll = [1 0 0; 0 cosd(roll) -sind(roll); 0 sind(roll) cosd(roll)];

    R = R_pitch * R_roll;
end