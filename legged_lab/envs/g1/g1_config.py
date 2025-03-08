from legged_lab.envs.base.base_env_config import (
    BaseEnvCfg, BaseAgentCfg, SceneCfg, RobotCfg, DomainRandCfg,
    RewardCfg, HeightScannerCfg, AddRigidBodyMassCfg, PhysxCfg, SimCfg
)
from legged_lab.assets.unitree import G1_CFG
from legged_lab.terrains import GRAVEL_TERRAINS_CFG
from isaaclab.managers import RewardTermCfg as RewTerm
import legged_lab.mdp as mdp
from isaaclab.managers.scene_entity_cfg import SceneEntityCfg
from isaaclab.utils import configclass


@configclass
class G1SceneCfg(SceneCfg):
    height_scanner: HeightScannerCfg = HeightScannerCfg(
        enable_height_scan=False,
        prim_body_name="torso_link"
    )
    robot: str = G1_CFG
    terrain_type: str = "generator"
    terrain_generator: str = GRAVEL_TERRAINS_CFG


@configclass
class G1RobotCfg(RobotCfg):
    terminate_contacts_body_names: list = [".*torso.*"]
    feet_names: list = [".*ankle_roll.*"]


@configclass
class G1DomainRandCfg(DomainRandCfg):
    add_rigid_body_mass: AddRigidBodyMassCfg = AddRigidBodyMassCfg(
        enable=True,
        params={
            "body_names": [".*torso.*"],
            "mass_distribution_params": (-5.0, 5.0),
            "operation": "add"
        }
    )


@configclass
class G1RewardCfg(RewardCfg):
    track_lin_vel_xy_exp = RewTerm(func=mdp.track_lin_vel_xy_yaw_frame_exp, weight=1.5, params={"std": 0.5}, )
    track_ang_vel_z_exp = RewTerm(func=mdp.track_ang_vel_z_world_exp, weight=1.5, params={"std": 0.5})
    lin_vel_z_l2 = RewTerm(func=mdp.lin_vel_z_l2, weight=-0.25)
    ang_vel_xy_l2 = RewTerm(func=mdp.ang_vel_xy_l2, weight=-0.05)
    energy = RewTerm(func=mdp.energy, weight=-1e-3)
    dof_acc_l2 = RewTerm(func=mdp.joint_acc_l2, weight=-2.5e-7)
    action_rate_l2 = RewTerm(func=mdp.action_rate_l2, weight=-0.01)
    undesired_contacts = RewTerm(func=mdp.undesired_contacts, weight=-1.0, params={"sensor_cfg": SceneEntityCfg("contact_sensor", body_names="(?!.*ankle.*).*"), "threshold": 1.0}, )
    fly = RewTerm(func=mdp.fly, weight=-1.0, params={"sensor_cfg": SceneEntityCfg("contact_sensor", body_names=".*ankle.*"), "threshold": 1.0})
    body_orientation_l2 = RewTerm(func=mdp.body_orientation_l2, params={"asset_cfg": SceneEntityCfg("robot", body_names=".*torso.*")}, weight=-2.0)
    flat_orientation_l2 = RewTerm(func=mdp.flat_orientation_l2, weight=-1.0)
    termination_penalty = RewTerm(func=mdp.is_terminated, weight=-200.0)
    feet_air_time = RewTerm(func=mdp.feet_air_time_positive_biped, weight=0.15, params={"sensor_cfg": SceneEntityCfg("contact_sensor", body_names=".*ankle_roll.*"), "threshold": 0.4, }, )
    feet_slide = RewTerm(func=mdp.feet_slide, weight=-0.25, params={"sensor_cfg": SceneEntityCfg("contact_sensor", body_names=".*ankle_roll.*"), "asset_cfg": SceneEntityCfg("robot", body_names=".*_ankle_roll.*"), },)
    feet_force = RewTerm(func=mdp.body_force, weight=-3e-3, params={"sensor_cfg": SceneEntityCfg("contact_sensor", body_names=".*ankle_roll.*"), "threshold": 500, "max_reward": 400},)
    feet_stumble = RewTerm(func=mdp.feet_stumble, weight=-2.0, params={"sensor_cfg": SceneEntityCfg("contact_sensor", body_names=".*ankle_roll.*")}, )
    dof_pos_limits = RewTerm(func=mdp.joint_pos_limits, weight=-2.0)
    joint_deviation_hip = RewTerm(func=mdp.joint_deviation_l1, weight=-0.15, params={"asset_cfg": SceneEntityCfg("robot", joint_names=[".*_hip_yaw.*", ".*_hip_roll.*", ".*_shoulder_pitch.*", ".*_elbow.*"])}, )
    joint_deviation_arms = RewTerm(func=mdp.joint_deviation_l1, weight=-0.2, params={"asset_cfg": SceneEntityCfg("robot", joint_names=[".*waist.*", ".*_shoulder_roll.*", ".*_shoulder_yaw.*", ".*_wrist.*"])})
    joint_deviation_legs = RewTerm(func=mdp.joint_deviation_l1, weight=-0.02, params={"asset_cfg": SceneEntityCfg("robot", joint_names=[".*_hip_pitch.*", ".*_knee.*", ".*ankle.*"])})


@configclass
class G1FlatEnvCfg(BaseEnvCfg):
    scene: G1SceneCfg = G1SceneCfg()
    robot: G1RobotCfg = G1RobotCfg()
    domain_rand: G1DomainRandCfg = G1DomainRandCfg()
    reward: G1RewardCfg = G1RewardCfg()


@configclass
class G1FlatAgentCfg(BaseAgentCfg):
    experiment_name: str = "g1_flat"
    wandb_project: str = "g1_flat"
