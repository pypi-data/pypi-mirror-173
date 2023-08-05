import yaml


async def execute_helm_command(hub, ctx, commands, flags, kvflags):
    cmd = hub.tool.helm.command_utils.prepare_command(ctx, commands, flags, kvflags)
    cmd_string = " ".join(cmd)
    cmd_ret = await hub.exec.cmd.run(
        cmd=cmd_string,
        python_shell=True,
    )
    return cmd_ret


async def install_release(hub, ctx, release_name, chart, flags, kvflags):
    commands = ["install", release_name, chart]
    return await __exec_cmd(hub, ctx, commands, flags, kvflags)


async def upgrade_release(hub, ctx, release_name, chart, flags, kvflags):
    commands = ["upgrade", release_name, chart]
    return await __exec_cmd(hub, ctx, commands, flags, kvflags)


async def uninstall_release(hub, ctx, release_name, namespace):
    commands = ["uninstall", release_name]
    kvflags = {"namespace": namespace}
    return await __exec_cmd(hub, ctx, commands, flags=[], kvflags=kvflags)


async def __exec_cmd(hub, ctx, commands, flags, kvflags):
    result = dict(comment=(), result=True, ret=None)
    cmd_ret = await hub.exec.helm.release.execute_helm_command(
        ctx, commands, flags, kvflags
    )
    if not cmd_ret["result"] or cmd_ret.ret["stderr"]:
        result["comment"] = cmd_ret["comment"]
        result["result"] = False
        return result
    result["ret"] = cmd_ret.ret["stdout"]
    return result


async def list_releases(hub, ctx, resource_id: str = None, namespace: str = None):
    result = dict(comment=(), result=True, ret=None)
    commands = ["list"]
    kvflags = {"output": "yaml"}
    flags = []

    if namespace:
        kvflags["namespace"] = namespace
    else:
        flags.append("all-namespaces")

    if resource_id:
        kvflags["filter"] = resource_id

    list_release_ret = await hub.exec.helm.release.execute_helm_command(
        ctx, commands, flags, kvflags
    )

    if not list_release_ret["result"] or list_release_ret.ret["stderr"]:
        result["comment"] = list_release_ret["comment"]
        result["result"] = False
    else:
        result["ret"] = yaml.load(list_release_ret.ret["stdout"], Loader=yaml.Loader)

    return result


async def get_release_values(hub, ctx, release):
    result = dict(comment=(), result=True, ret=None)
    commands = ["get", "values", release["name"]]
    kvflags = {"namespace": release["namespace"], "output": "yaml"}

    values_ret = await hub.exec.helm.release.execute_helm_command(
        ctx, commands, flags=[], kvflags=kvflags
    )
    if not values_ret["result"] or values_ret.ret["stderr"]:
        result["comment"] = values_ret["comment"]
        result["result"] = False
        return result

    if values_ret.ret["stdout"].rstrip().endswith("null"):
        values_ret.ret["stdout"] = values_ret.ret["stdout"].replace("null", "")

    result["ret"] = values_ret.ret["stdout"]
    return result
