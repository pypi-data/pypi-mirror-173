from instapy2 import comments
from .instapy2_base import InstaPy2Base

from typing import List, Union

import random

class InstaPy2(InstaPy2Base):
    def follow_commenters(self, amount: int = 10, usernames: List[str] = []):
        if not isinstance(usernames, list):
            usernames = [usernames]

        for index, username in enumerate(iterable=usernames):
            print(f'[INFO]: Username [{index + 1}/{len(usernames)}]')
            print(f'[INFO]: {username}')

            media = self.medias_username(amount=1, username=username, randomize_media=False)[0]
            comments = self.session.media_comments(media_id=media.id)
            commenter_usernames = []
            for comment in comments:
                if comment.user.username not in commenter_usernames and comment.user.username != media.user.username and len(commenter_usernames) < amount:
                    commenter_usernames.append(comment.user.username)

            self.follow_usernames(usernames=commenter_usernames)


    def follow_likers(self, amount: int = 10, usernames: List[str] = []):
        if not isinstance(usernames, list):
            usernames = [usernames]

        for index, username in enumerate(iterable=usernames):
            print(f'[INFO]: Username [{index + 1}/{len(usernames)}]')
            print(f'[INFO]: {username}')

            media = self.medias_username(amount=1, username=username, randomize_media=False)[0]
            liker_usernames = [liker.username for liker in self.session.media_likers(media_id=media.id)]

            self.follow_usernames(usernames=liker_usernames)
            

    def follow_locations(self, amount: int = 50, locations: List[int] = [], randomize_media: bool = False, skip_top: bool = True):
        followed_count = 0
        for index, location in enumerate(iterable=locations):
            print(f'[INFO]: Location [{index + 1}/{len(locations)}]')
            print(f'[INFO]: {location}')

            location_info = self.session.location_info(location_pk=location)
            location_name = location_info.name if location_info.name is not None else 'Unavailable'

            medias = self.medias_location(amount=amount, location=location_info.pk, randomize_media=randomize_media, skip_top=skip_top)
            print(f'[INFO]: Found {len(medias)} media from {location_name}.')

            for index, media in enumerate(iterable=medias):
                if self.configuration.media.validated_for_interaction(media=media):
                    user_id = self.session.user_id_from_username(username=media.user.username)
                    relationship_status = self.session.user_friendship_v1(user_id=user_id)
                    if not relationship_status.following:
                        followed = self.configuration.follows.follow(user_id=user_id, username=media.user.username)
                        if followed:
                            followed_count += 1

        print(f'[INFO]: Followed {followed_count} of {len(medias)} users.')

    
    def follow_tags(self, amount: int = 50, tags: List[str] = [], randomize_media: bool = False, randomize_tags: bool = False, skip_top: bool = True):
        followed_count = 0
        tags = [tag.strip() for tag in tags] or []
        
        if randomize_tags:
            random.shuffle(x=tags)

        for index, tag in enumerate(iterable=tags):
            print(f'[INFO]: Tag [{index + 1}/{len(tags)}]')
            print(f'[INFO]: {tag}')

            medias = self.medias_tag(amount=amount, tag=tag, randomize_media=randomize_media, skip_top=skip_top)
            print(f'[INFO]: Found {len(medias)} media from {[media.user.username for media in medias]}.')

            for index, media in enumerate(iterable=medias):
                if self.configuration.media.validated_for_interaction(media=media):
                    user_id = self.session.user_id_from_username(username=media.user.username)
                    relationship_status = self.session.user_friendship_v1(user_id=user_id)

                    if (random.randint(a=0, b=100) <= self.configuration.follows.percentage) and not relationship_status.following:
                        followed = self.configuration.follows.follow(user_id=user_id, username=media.user.username)
                        if followed:
                            followed_count += 1

        print(f'[INFO]: Followed {followed_count} of {len(medias)} users.')
    
    
    def follow_usernames(self, usernames: List[str] = []):
        followed_count = 0
        for index, username in enumerate(iterable=usernames):
            print(f'[INFO]: Username [{index + 1}/{len(usernames)}]')
            print(f'[INFO]: {username}')

            user_id = self.session.user_id_from_username(username=username)
            relationship_status = self.session.user_friendship_v1(user_id=user_id)
            if not relationship_status.following:
                followed = self.configuration.follows.follow(user_id=user_id, username=username)
                if followed:
                    followed_count += 1
            else:
                print('[INFO]: Already following.')

            if followed:
                if self.configuration.interactions.enabled and self.configuration.likes.enabled:
                    interacting = random.randint(0, 100) <= self.configuration.interactions.percentage
                    if interacting:
                        self.interact_users(amount=self.configuration.interactions.amount, usernames=username, randomize_media=self.configuration.interactions.randomize)


        print(f'[INFO]: Followed {followed_count} of {len(usernames)} users.')
    
    
    def unfollow_usernames(self, amount: int = 10, usernames: List[str] = [], only_nonfollowers: bool = True, randomize_usernames: bool = False):
        unfollowed_count = 0
        user_ids = []
        [user_ids.append(user_id) for user_id in self.session.user_following(user_id=self.session.user_id, amount=amount).keys() if self.session.username_from_user_id(user_id=user_id) not in self.configuration.people.friends_to_skip] if len(usernames) == 0 else [user_ids.append(self.session.user_id_from_username(username=username)) for username in usernames]

        if randomize_usernames:
            random.shuffle(x=user_ids)

        for index, user_id in enumerate(iterable=user_ids):
            print(f'[INFO]: Username [{index + 1}/{len(user_ids)}]')
            print(f'[INFO]: {self.session.username_from_user_id(user_id=user_id)}')

            if only_nonfollowers and not self.session.user_friendship_v1(user_id=user_id).followed_by:
                unfollowed = self.configuration.follows.unfollow(user_id=user_id, username=self.session.username_from_user_id(user_id=user_id))
                if unfollowed:
                    unfollowed_count += 1
            else:
                unfollowed = self.configuration.follows.unfollow(user_id=user_id, username=self.session.username_from_user_id(user_id=user_id))
                if unfollowed_count:
                    unfollowed_count += 1

        print(f'[INFO]: Unfollowed {unfollowed_count} of {len(usernames)} users.')
    

    def like_feed(self, amount: int = 50, usernames: List[str] = [], randomize_likes: bool = False, unfollow: bool = False):
        if not isinstance(usernames, list):
            usernames = [usernames]

        for index, username in enumerate(iterable=usernames):
            print(f'[INFO]: Username [{index + 1}/{len(usernames)}]')
            print(f'[INFO]: {username}')

            medias = self.medias_username(amount=amount, username=username)

            for media in medias:
                if randomize_likes and random.choice([True, False]):
                    pass
                else:
                    if self.configuration.media.validated_for_interaction(media=media):
                        liked = self.configuration.likes.like(media=media)

                        if self.configuration.comments.enabled_for_liked_media or liked:
                            commenting = (random.randint(a=0, b=100) <= self.configuration.comments.percentage)
                            following = (random.randint(a=0, b=100) <= self.configuration.follows.percentage)

                            # comment
                            if self.configuration.comments.enabled and commenting and media.user.username not in self.configuration.people.friends_to_skip:
                                    try:
                                        commented = self.session.media_comment(media_id=media.id, text=random.choice(seq=self.configuration.comments.comments).format(media.user.username))
                                        print(f'[INFO]: Successfully commented on media: {media.code}' if commented is not None else '[ERROR]: Failed to comment on media.')
                                    except Exception as error:
                                        print(f'[ERROR]: {error}.')

                            # follow
                            if self.configuration.follows.enabled and following and media.user.username not in self.configuration.people.friends_to_skip:
                                if not self.configuration.people.following_user(media=media):    
                                    try:
                                        followed = self.session.user_follow(user_id=self.session.user_id_from_username(username=media.user.username))
                                        print(f'[INFO]: Successfully followed: {media.user.username}.' if followed else '[ERROR]: Failed to follow user.')
                                    except Exception as error:
                                        print(f'[ERROR]: {error}.')

                            if followed:
                                if self.configuration.interactions.enabled and self.configuration.likes.enabled:
                                    interacting = random.randint(0, 100) <= self.configuration.interactions.percentage
                                    if interacting:
                                        self.interact_users(amount=self.configuration.interactions.amount, usernames=username, randomize_media=self.configuration.interactions.randomize)


    def like_locations(self, amount: int = 50, locations: List[int] = [], randomize_media: bool = False, skip_top: bool = True):
        for index, location in enumerate(iterable=locations):
            print(f'[INFO]: Location [{index + 1}/{len(locations)}]')
            print(f'[INFO]: {location}')

            medias = self.medias_location(amount=amount, location=location, randomize_media=randomize_media, skip_top=skip_top)
            for media in medias:
                if self.configuration.media.validated_for_interaction(media=media):
                    # like
                    try:
                        liked = self.session.media_like(media_id=media.id)
                        print(f'[INFO]: Successfully liked media: {media.code}')
                    except Exception as error:
                        print(f'[ERROR]: {error}.')
                        
                    if self.configuration.comments.enabled_for_liked_media or liked:
                        commenting = (random.randint(a=0, b=100) <= self.configuration.comments.percentage)
                        following = (random.randint(a=0, b=100) <= self.configuration.follows.percentage)

                        # comment
                        if self.configuration.comments.enabled and commenting and media.user.username not in self.configuration.people.friends_to_skip:
                                try:
                                    commented = self.session.media_comment(media_id=media.id, text=random.choice(seq=self.configuration.comments.comments).format(media.user.username))
                                    print(f'[INFO]: Successfully commented on media: {media.code}' if commented is not None else '[ERROR]: Failed to comment on media.')
                                except Exception as error:
                                    print(f'[ERROR]: {error}.')

                        # follow
                        if not self.configuration.people.following_user(media=media):
                            if self.configuration.follows.enabled and following and media.user.username not in self.configuration.people.friends_to_skip:
                                try:
                                    followed = self.session.user_follow(user_id=self.session.user_id_from_username(username=media.user.username))
                                    print(f'[INFO]: Successfully followed: {media.user.username}.' if followed else '[ERROR]: Failed to follow user.')
                                except Exception as error:
                                    print(f'[ERROR]: {error}.')
                        else:
                                print('[ERROR]: Already following user.')


    def like_tags(self, amount: int = 50, tags: List[str] = [], randomize_media: bool = False, randomize_tags: bool = False, skip_top: bool = True):
        tags = [tag.strip() for tag in tags] or []
        
        if randomize_tags:
            random.shuffle(x=tags)

        for index, tag in enumerate(iterable=tags):
            print(f'[INFO]: Tag [{index + 1}/{len(tags)}]')
            print(f'[INFO]: {tag}')

            medias = self.medias_tag(amount=amount, tag=tag, randomize_media=randomize_media, skip_top=skip_top)
            print(f'[INFO]: Found {len(medias)} media.')

            for media in medias:
                if self.configuration.media.validated_for_interaction(media=media):
                    # like
                    try:
                        liked = self.session.media_like(media_id=media.id)
                        print(f'[INFO]: Successfully liked media: {media.code}')
                    except Exception as error:
                        print(f'[ERROR]: {error}.')
                        
                    if self.configuration.comments.enabled_for_liked_media or liked:
                        commenting = (random.randint(a=0, b=100) <= self.configuration.comments.percentage)
                        following = (random.randint(a=0, b=100) <= self.configuration.follows.percentage)

                        # comment
                        if self.configuration.comments.enabled and commenting and media.user.username not in self.configuration.people.friends_to_skip:
                                try:
                                    commented = self.session.media_comment(media_id=media.id, text=random.choice(seq=self.configuration.comments.comments).format(media.user.username))
                                    print(f'[INFO]: Successfully commented on media: {media.code}' if commented is not None else '[ERROR]: Failed to comment on media.')
                                except Exception as error:
                                    print(f'[ERROR]: {error}.')

                        # follow
                        if not self.configuration.people.following_user(media=media):
                            if self.configuration.follows.enabled and following and media.user.username not in self.configuration.people.friends_to_skip:
                                try:
                                    followed = self.session.user_follow(user_id=self.session.user_id_from_username(username=media.user.username))
                                    print(f'[INFO]: Successfully followed: {media.user.username}.' if followed else '[ERROR]: Failed to follow user.')
                                except Exception as error:
                                    print(f'[ERROR]: {error}.')
                        else:
                                print('[ERROR]: Already following user.')

                        if followed:
                                if self.configuration.interactions.enabled and self.configuration.likes.enabled:
                                    interacting = random.randint(0, 100) <= self.configuration.interactions.percentage
                                    if interacting:
                                        self.interact_users(amount=self.configuration.interactions.amount, usernames=username, randomize_media=self.configuration.interactions.randomize)

    
    def like_users(self, amount: int = 10, usernames: List[str] = [], randomize_media: bool = False):
        if not isinstance(usernames, list):
            usernames = [usernames]

        for index, username in enumerate(iterable=usernames):
            print(f'[INFO]: Username [{index + 1}/{len(usernames)}]')
            print(f'[INFO]: {username}')

            medias = self.medias_username(amount=amount, username=username, randomize_media=randomize_media)
            print(f'[INFO]: Found {len(medias)} media.')

            for media in medias:
                if self.configuration.media.validated_for_interaction(media=media):
                    liked = self.configuration.likes.like(media=media)
                        
                    if self.configuration.comments.enabled_for_liked_media or liked:
                        commenting = (random.randint(a=0, b=100) <= self.configuration.comments.percentage)
                        following = (random.randint(a=0, b=100) <= self.configuration.follows.percentage)

                        # comment
                        if self.configuration.comments.enabled and commenting and media.user.username not in self.configuration.people.friends_to_skip:
                                try:
                                    commented = self.session.media_comment(media_id=media.id, text=random.choice(seq=self.configuration.comments.comments).format(media.user.username))
                                    print(f'[INFO]: Successfully commented on media: {media.code}' if commented is not None else '[ERROR]: Failed to comment on media.')
                                except Exception as error:
                                    print(f'[ERROR]: {error}.')

                        # follow
                        if self.configuration.follows.enabled and following and media.user.username not in self.configuration.people.friends_to_skip:
                            if not self.configuration.people.following_user(media=media):    
                                try:
                                    followed = self.session.user_follow(user_id=self.session.user_id_from_username(username=media.user.username))
                                    print(f'[INFO]: Successfully followed: {media.user.username}.' if followed else '[ERROR]: Failed to follow user.')
                                except Exception as error:
                                    print(f'[ERROR]: {error}.')


    def interact_users(self, amount: int = 10, usernames: List[str] = [], randomize_media: bool = False):
        if not isinstance(usernames, list):
            usernames = [usernames]

        commented_count = 0
        followed_count = 0
        liked_count = 0


        for index, username in enumerate(iterable=usernames):
            print(f'[INFO]: Username [{index + 1}/{len(usernames)}]')
            print(f'[INFO]: {username}')

            if username not in self.configuration.people.friends_to_skip:
                medias = self.medias_username(amount=amount, username=username, randomize_media=randomize_media)

                following = random.randint(0, 100) <= self.configuration.follows.percentage

                for index, media in enumerate(iterable=medias):
                    if self.configuration.media.validated_for_interaction(media=media):
                        if index > 0:
                            liking = random.randint(a=0, b=100) <= self.configuration.likes.percentage
                            commenting = random.randint(a=0, b=100) <= self.configuration.comments.percentage

                            if self.configuration.likes.enabled and liking:
                                liked = self.configuration.likes.like(media=media)
                                if liked:
                                    liked_count += 1

                                if commenting and liked or self.configuration.comments.enabled_for_liked_media:
                                    try:
                                        commented = self.session.media_comment(media_id=media.id, text=random.choice(seq=self.configuration.comments.comments).format(media.user.username))
                                        print(f'[INFO]: Successfully commented on media: {media.code}' if commented is not None else '[ERROR]: Failed to comment on media.')
                                        if commented:
                                            commented_count += 1
                                    except Exception as error:
                                        print(f'[ERROR]: {error}.')

                if following: # what is dont_follow_inap_post?
                    followed = self.configuration.follows.follow(user_id=self.session.user_id_from_username(username=username))
                    if followed:
                        followed_count += 1

        print(f'[INFO]: Commented on {commented_count} media.')
        print(f'[INFO]: Followed {followed_count} users.')
        print(f'[INFO]: Liked {liked_count} media.')