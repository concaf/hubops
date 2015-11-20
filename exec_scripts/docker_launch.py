# /usr/bin/python3

from docker import Client
import json
import requests, sys

sys.path.append("/root/hubops")
from config.docker_config import docker_config
from sys import argv


def search_images_local(image_list, user_repotag):
    local_repotags = list()
    for image_name in image_list:
        for separate_tags in image_name['RepoTags']:
            local_repotags.append(separate_tags)

    if user_repotag in local_repotags:
        return True
    else:
        return False


def search_images_name_remote(name_to_search, opened_client, controller_official):
    hub_results = opened_client.search(name_to_search)
    found_list = list([''])
    for filtered_results in hub_results:
        if (controller_official == "o") and (filtered_results['is_official']):
            print("Found {}".format(filtered_results['name']))
            found_list.append(filtered_results['name'])
        elif controller_official == "u":
            print("Found {}".format(filtered_results['name']))
            found_list.append(filtered_results['name'])
    return found_list


def pull_process(image_to_pull, opened_client):
    for pull_progress in opened_client.pull(image_to_pull, stream=True):
        for pull_element, pull_key in json.loads(pull_progress.decode()).items():
            if pull_element == 'id':
                print("For image id {}:\n".format(pull_key.lower()), end=' ')
            if pull_element == 'status':
                print("The current status is {}\n\n".format(pull_key.lower()))


def start_container(image_repository, image_repository_tags):
    # Establishing connection
    client_instance = Client(base_url=docker_config())

    user_repotag = "{}:{}".format(image_repository, image_repository_tags)

    # Searching for images locally
    local_exists = search_images_local(client_instance.images(), user_repotag)

    if local_exists:
        print("Found the image {} locally, launching now.".format(user_repotag))
    elif not local_exists:
        print("The image does not exist locally. "
              "HubOps will now search for images on Docker Hub.\n")

        # User wants official or unofficial images?
        while True:
            official_or_not = input("Search for official images or unofficial images?\n"
                                    "Official(O)\n"
                                    "Unofficial(U)\n").lower()
            if official_or_not in list("ou"):
                break

        found_list = search_images_name_remote(image_repository, client_instance, official_or_not)

        if len(found_list) == 1:
            print("No official image found for {}".format(image_repository))
        else:
            print("Official images on Docker Hub:")
            for official_name in found_list[1:]:
                print("{}. {}".format(found_list.index(official_name), official_name))

            image_index_to_pull = int(input("\nWhich image would you like to work on from the above list?\n"
                                            "Enter the number which appears with the image name.\n"
                                            "e.g. If you want to pull\n"
                                            "3. tomcat7\n"
                                            "Then type in 3 and press the Enter key.\n"))

            image_name_to_pull = found_list[image_index_to_pull]
            image_tags = list([''])
            image_tags_request = requests.get(
                "https://registry.hub.docker.com/v1/repositories/{}/tags".format(image_name_to_pull))
            for image_tag_details in image_tags_request.json():
                image_tags.append(image_tag_details['name'])

            print("\n\nThe tags available for {} on Docker Hub are:\n".format(image_name_to_pull))
            for tag_name in image_tags[1:]:
                print("{}. {}".format(image_tags.index(tag_name), tag_name))

            image_tag_to_pull = image_tags[
                int(input("Which {} tag do you want to work with?\n".format(image_name_to_pull)))]

            image_to_pull = "{}:{}".format(image_name_to_pull, image_tag_to_pull)
            print("Pulling {} now...".format(image_to_pull))
            pull_process(image_to_pull, client_instance)


if __name__ == '__main__':
    try:
        image_name_argv = argv[1]
    except IndexError:
        image_name_argv = "centos"
        print("No image name entered. Setting {} by default.".format(image_name_argv))

    try:
        image_tag_argv = argv[2]
    except IndexError:
        image_tag_argv = "latest"
        print("No image tag entered. Setting {} by default.".format(image_tag_argv))

    start_container(image_name_argv, image_tag_argv)
