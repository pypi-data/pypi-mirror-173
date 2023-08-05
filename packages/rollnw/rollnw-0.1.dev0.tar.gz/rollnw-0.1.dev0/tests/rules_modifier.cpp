#include <catch2/catch_all.hpp>

#include <nw/components/Creature.hpp>
#include <nw/kernel/Objects.hpp>
#include <nw/kernel/Rules.hpp>
#include <nw/rules/Feat.hpp>
#include <nw/rules/Modifier.hpp>
#include <nw/rules/system.hpp>
#include <nwn1/Profile.hpp>
#include <nwn1/rules.hpp>

namespace fs = std::filesystem;
namespace nwk = nw::kernel;

TEST_CASE("modifier", "[rules]")
{
    auto ent = nw::kernel::objects().load<nw::Creature>(fs::path("../tests/test_data/user/development/pl_agent_001.utc"));
    REQUIRE(ent);
    ent->levels.entries[0].id = nwn1::class_type_pale_master;

    auto is_pm = nw::Requirement{{nwn1::qual::class_level(nwn1::class_type_pale_master, 1)}};

    auto pm_ac = [](const nw::ObjectBase* obj) -> nw::ModifierResult {
        auto cre = obj->as_creature();
        if (!cre) {
            return 0;
        }
        auto pm_level = cre->levels.level_by_class(nwn1::class_type_pale_master);
        return pm_level > 0 ? ((pm_level / 4) + 1) * 2 : 0;
    };

    auto mod2 = nwn1::mod::armor_class(nwn1::ac_natural, pm_ac,
        "dnd-3.0-palemaster-ac", nw::ModifierSource::class_);

    int res = 0;
    REQUIRE(nwk::rules().calculate(ent, mod2,
        [&res](int value) {
            res += value;
        }));
    REQUIRE(res == 6);

    // False because output size mismatch
    REQUIRE_FALSE(nwk::rules().calculate(ent, mod2,
        [&res](int value, float) {
            res += value;
        }));

    // False because output mismatch
    float res2 = 0.0f;
    REQUIRE_FALSE(nwk::rules().calculate(ent, mod2,
        [&res2](float value) {
            res2 += value;
        }));
}

TEST_CASE("modifier kernel", "[rules]")
{
    auto mod = nwk::load_module("test_data/user/modules/DockerDemo.mod");
    REQUIRE(mod);

    auto ent = nwk::objects().load<nw::Creature>(fs::path("test_data/user/development/pl_agent_001.utc"));
    REQUIRE(ent);
    ent->levels.entries[0].id = nwn1::class_type_pale_master;

    int res = 0;
    nwk::rules().calculate(ent, nwn1::mod_type_armor_class, nwn1::ac_natural,
        [&res](int value) {
            res += value;
        });
    REQUIRE(res == 6);

    auto pm_ac_nerf = [](const nw::ObjectBase* obj) -> nw::ModifierResult {
        auto cre = obj->as_creature();
        if (!cre) {
            return 0;
        }
        auto pm_level = cre->levels.level_by_class(nwn1::class_type_pale_master);
        return ((pm_level / 4) + 1);
    };

    // Get rid of any requirement
    REQUIRE(nwk::rules().replace("dnd-3.0-palemaster-ac", nw::Requirement{}));
    // Set nerf
    REQUIRE(nwk::rules().replace("dnd-3.0-palemaster-ac", nw::ModifierInputs{pm_ac_nerf}));
    res = 0;
    REQUIRE(nwk::rules().calculate(ent, nwn1::mod_type_armor_class, nwn1::ac_natural,
        [&res](int value) {
            res += value;
        }));
    REQUIRE(res == 3);

    REQUIRE(nwk::rules().remove("dnd-3.0-palemaster-*"));
    res = 0;
    REQUIRE(nwk::rules().calculate(ent, nwn1::mod_type_armor_class, nwn1::ac_natural,
        [&res](int value) {
            res += value;
        }));
    REQUIRE(res == 0);

    nwk::unload_module();
}

TEST_CASE("modifier kernel 2", "[rules]")
{
    auto mod = nwk::load_module("test_data/user/modules/DockerDemo.mod");
    REQUIRE(mod);

    auto ent = nwk::objects().load<nw::Creature>(fs::path("test_data/user/development/pl_agent_001.utc"));
    REQUIRE(ent);
    ent->stats.add_feat(nwn1::feat_epic_toughness_1);
    ent->stats.add_feat(nwn1::feat_epic_toughness_2);
    ent->stats.add_feat(nwn1::feat_epic_toughness_3);

    auto [highest, nth] = nwn1::has_feat_successor(ent, nwn1::feat_epic_toughness_1);
    REQUIRE(highest == nwn1::feat_epic_toughness_4);
    REQUIRE(nth == 4);

    int res = 0;
    REQUIRE(nwk::rules().calculate(ent, nwn1::mod_type_hitpoints,
        [&res](int value) {
            res += value;
        }));
    REQUIRE(res == 80);

    nwk::unload_module();
}

TEST_CASE("modifier kernel 3", "[rules]")
{
    auto mod = nwk::load_module("test_data/user/modules/DockerDemo.mod");
    REQUIRE(mod);

    auto ent = nwk::objects().load<nw::Creature>(fs::path("test_data/user/development/pl_agent_001.utc"));
    REQUIRE(ent);
    ent->stats.add_feat(nwn1::feat_resist_energy_acid);

    int res = 0;
    REQUIRE(nwk::rules().calculate(
        ent, nwn1::mod_type_dmg_resistance,
        nwn1::damage_type_acid,
        [&res](int value) {
            res += value;
        }));

    REQUIRE(res == 5);

    ent->stats.add_feat(nwn1::feat_epic_energy_resistance_acid_1);
    ent->stats.add_feat(nwn1::feat_epic_energy_resistance_acid_2);
    res = 0;
    REQUIRE(nwk::rules().calculate(ent, nwn1::mod_type_dmg_resistance,
        nwn1::damage_type_acid,
        [&res](int value) {
            res += value;
        }));

    REQUIRE(res == 20);

    nwk::unload_module();
}
